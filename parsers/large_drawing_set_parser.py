"""
Large Drawing Set Parser
Handles 1500+ page architectural drawing sets to find roofing details.

Two-stage approach:
1. Python filtering - eliminates ~95% of irrelevant pages based on sheet numbers and keywords
2. AI vision analysis - uses Claude/OpenAI vision to analyze filtered pages

Author: Based on CLAUDE.md standards
"""
import os
import re
import json
import logging
import tempfile
import base64
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

import pdfplumber

# Optional imports for AI vision
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ============================================================================
# DATA CLASSES
# ============================================================================

class SheetCategory(Enum):
    """Architectural drawing sheet categories per AIA standards"""
    GENERAL = "G"           # General (cover, index, symbols)
    CIVIL = "C"             # Civil
    LANDSCAPE = "L"         # Landscape
    STRUCTURAL = "S"        # Structural
    ARCHITECTURAL = "A"     # Architectural
    INTERIORS = "I"         # Interiors
    EQUIPMENT = "Q"         # Equipment
    FIRE_PROTECTION = "F"   # Fire Protection
    PLUMBING = "P"          # Plumbing
    MECHANICAL = "M"        # Mechanical
    ELECTRICAL = "E"        # Electrical
    UNKNOWN = "?"


@dataclass
class SheetInfo:
    """Information extracted from a drawing sheet"""
    page_number: int
    sheet_number: str
    sheet_title: str = ""
    category: SheetCategory = SheetCategory.UNKNOWN
    is_roof_related: bool = False
    roof_relevance_score: float = 0.0
    relevance_reasons: List[str] = field(default_factory=list)
    extracted_text: str = ""
    text_preview: str = ""
    ai_analysis: Optional[Dict] = None

    def to_dict(self) -> Dict:
        result = asdict(self)
        result['category'] = self.category.value
        return result


@dataclass
class RoofDetail:
    """Structured roofing detail extracted from drawings"""
    sheet_number: str
    page_number: int
    detail_type: str  # "ROOF PLAN", "ROOF DETAIL", "ROOF SECTION", etc.
    detail_number: str = ""
    title: str = ""
    scale: str = ""

    # Roof elements
    drains: int = 0
    scuppers: int = 0
    rtus: int = 0
    penetrations: int = 0
    skylights: int = 0
    hatches: int = 0

    # Area info
    roof_area_name: str = ""
    square_footage: Optional[int] = None

    # Materials/systems (if visible)
    membrane_type: str = ""
    insulation_type: str = ""

    # References to other details
    detail_references: List[str] = field(default_factory=list)
    spec_references: List[str] = field(default_factory=list)

    # AI analysis
    ai_description: str = ""
    ai_confidence: float = 0.0

    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================================
# SHEET NUMBER PATTERNS - AIA STANDARDS
# ============================================================================

# Roof-related sheet patterns
ROOF_SHEET_PATTERNS = [
    # A5xx series - Roof plans (AIA standard)
    r'^A-?5\d{2}',
    r'^A5\.\d+',
    # Explicit roof mentions
    r'ROOF\s*PLAN',
    r'ROOF\s*DETAIL',
    r'ROOF\s*SECTION',
    r'ROOFING',
    r'R-\d+',
    r'RF-?\d+',
    # Architectural details that may include roof
    r'^A-?[89]\d{2}',  # A8xx, A9xx often details
    r'^A[89]\.\d+',
]

# Keywords that indicate roof relevance (weighted)
ROOF_KEYWORDS = {
    # High relevance (score 1.0)
    'roof plan': 1.0,
    'roof detail': 1.0,
    'roof section': 1.0,
    'roofing': 1.0,
    'roof drain': 1.0,
    'roof hatch': 1.0,
    'parapet': 0.9,
    'coping': 0.9,
    'flashing': 0.9,
    'membrane': 0.8,
    'tpo': 0.9,
    'epdm': 0.9,
    'pvc roofing': 0.9,
    'built-up roof': 0.9,
    'bur': 0.7,
    'modified bitumen': 0.9,
    'standing seam': 0.9,

    # Medium relevance (score 0.5-0.7)
    'scupper': 0.7,
    'overflow': 0.6,
    'crickets': 0.7,
    'saddle': 0.6,
    'tapered insulation': 0.8,
    'polyiso': 0.7,
    'cover board': 0.7,
    'vapor barrier': 0.6,
    'air barrier': 0.5,
    'rtu': 0.6,
    'curb': 0.5,
    'penetration': 0.5,
    'pitch pocket': 0.7,
    'cant strip': 0.7,
    'edge metal': 0.7,
    'gravel stop': 0.7,
    'fascia': 0.5,
    'soffit': 0.4,

    # Low relevance (supporting context)
    'waterproof': 0.4,
    'drainage': 0.4,
    'slope': 0.3,
    'deck': 0.3,
    'insulation': 0.3,
    'expansion joint': 0.5,
    'control joint': 0.4,
}

# Sheet categories to prioritize
PRIORITY_CATEGORIES = [
    SheetCategory.ARCHITECTURAL,
    SheetCategory.STRUCTURAL,  # Structural often has roof framing
]

# Exclude these from analysis (not roof-related)
EXCLUDE_SHEET_PATTERNS = [
    r'^A-?1\d{2}',  # A1xx = Floor plans (ground level)
    r'^A1\.\d+',
    r'^A-?2\d{2}',  # A2xx = Elevations (may include but usually exterior views)
    r'^A-?3\d{2}',  # A3xx = Building sections (may include roof sections)
    r'^E-?\d+',     # Electrical
    r'^P-?\d+',     # Plumbing (except roof drains)
    r'^M-?\d+',     # Mechanical
    r'^G-?\d+',     # General
    r'^L-?\d+',     # Landscape
    r'^C-?\d+',     # Civil
]


# ============================================================================
# STAGE 1: PYTHON FILTERING
# ============================================================================

class DrawingSetFilter:
    """
    Filters large drawing sets to find roof-related pages.
    Uses sheet numbers, title block extraction, and keyword analysis.
    """

    def __init__(self, pdf_path: str, min_relevance_score: float = 0.3):
        self.pdf_path = pdf_path
        self.min_relevance_score = min_relevance_score
        self.sheets: List[SheetInfo] = []
        self.filtered_sheets: List[SheetInfo] = []
        self.stats = {
            'total_pages': 0,
            'pages_analyzed': 0,
            'roof_related_pages': 0,
            'processing_time_seconds': 0
        }

    def analyze_pdf(self, max_pages: Optional[int] = None) -> List[SheetInfo]:
        """
        Analyze PDF to identify roof-related sheets.

        Args:
            max_pages: Optional limit for testing with large files

        Returns:
            List of SheetInfo for roof-related pages
        """
        import time
        import PyPDF2
        start_time = time.time()

        logger.info(f"Opening PDF: {self.pdf_path}")

        # First, get total page count using PyPDF2 (more robust)
        try:
            with open(self.pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                total_pages = len(pdf_reader.pages)
                self.stats['total_pages'] = total_pages
        except Exception as e:
            logger.error(f"Error reading PDF with PyPDF2: {e}")
            total_pages = 0
            self.stats['total_pages'] = 0

        # Process pages individually to handle malformed pages
        pages_to_analyze = min(max_pages, total_pages) if max_pages else total_pages
        logger.info(f"Analyzing {pages_to_analyze} of {total_pages} pages...")

        # Use PyPDF2 for text extraction (handles malformed pages better)
        try:
            with open(self.pdf_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)

                for page_num in range(1, pages_to_analyze + 1):
                    if page_num % 100 == 0:
                        logger.info(f"  Processing page {page_num}/{pages_to_analyze}...")

                    try:
                        page = pdf_reader.pages[page_num - 1]
                        text = page.extract_text() or ""
                        sheet_info = self._analyze_page_text(text, page_num)
                        self.sheets.append(sheet_info)

                        if sheet_info.is_roof_related:
                            self.filtered_sheets.append(sheet_info)
                    except Exception as e:
                        logger.warning(f"  Skipping page {page_num} due to error: {e}")
                        # Create minimal sheet info for skipped pages
                        sheet_info = SheetInfo(
                            page_number=page_num,
                            sheet_number=f"PAGE-{page_num}",
                            is_roof_related=False,
                            roof_relevance_score=0.0
                        )
                        self.sheets.append(sheet_info)

        except Exception as e:
            logger.error(f"Error processing PDF: {e}")

        self.stats['pages_analyzed'] = len(self.sheets)
        self.stats['roof_related_pages'] = len(self.filtered_sheets)

        self.stats['processing_time_seconds'] = round(time.time() - start_time, 2)

        logger.info(f"Analysis complete: {self.stats['roof_related_pages']} roof-related pages found")
        logger.info(f"Filtered {100 - (self.stats['roof_related_pages']/self.stats['pages_analyzed']*100):.1f}% of pages")

        return self.filtered_sheets

    def _analyze_page_text(self, text: str, page_num: int) -> SheetInfo:
        """Analyze page text to determine roof relevance."""
        text_lower = text.lower()

        # Extract sheet number from title block
        sheet_number = self._extract_sheet_number_from_text(text, page_num)

        # Extract sheet title
        sheet_title = self._extract_sheet_title(text)

        # Determine category from sheet number
        category = self._categorize_sheet(sheet_number)

        # Calculate roof relevance score
        relevance_score, reasons = self._calculate_relevance(
            sheet_number, sheet_title, text_lower, category
        )

        is_roof_related = relevance_score >= self.min_relevance_score

        return SheetInfo(
            page_number=page_num,
            sheet_number=sheet_number,
            sheet_title=sheet_title,
            category=category,
            is_roof_related=is_roof_related,
            roof_relevance_score=relevance_score,
            relevance_reasons=reasons,
            extracted_text=text,
            text_preview=text[:500] if text else ""
        )

    def _extract_sheet_number_from_text(self, text: str, page_num: int) -> str:
        """Extract sheet number from title block text."""
        # Common sheet number patterns
        patterns = [
            r'\b([A-Z]-?\d{3}(?:\.\d+)?)\b',  # A-501, A501, A5.01
            r'\bSheet\s*(?:No\.?|#)?\s*([A-Z0-9.-]+)',
            r'\b([A-Z]{1,2}\d{1,2}\.\d{1,2})\b',  # A5.01, AR5.1
            r'^([A-Z]-?\d+)',  # Start of line sheet numbers
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                # Return the most likely sheet number (usually appears multiple times)
                from collections import Counter
                counter = Counter(matches)
                return counter.most_common(1)[0][0].upper()

        return f"PAGE-{page_num}"

    def _extract_sheet_title(self, text: str) -> str:
        """Extract sheet title from the page."""
        # Look for common title patterns
        patterns = [
            r'(?:ROOF\s+PLAN|ROOFING\s+PLAN)[^\n]*',
            r'(?:ROOF\s+DETAIL|ROOFING\s+DETAIL)[S]?[^\n]*',
            r'(?:ROOF\s+SECTION)[S]?[^\n]*',
            r'(?:ENLARGED\s+ROOF)[^\n]*',
            r'\b(LEVEL\s+\d+\s+ROOF)[^\n]*',
            r'\b(HIGH\s+ROOF|LOW\s+ROOF|MAIN\s+ROOF)[^\n]*',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()[:100]

        return ""

    def _categorize_sheet(self, sheet_number: str) -> SheetCategory:
        """Categorize sheet based on number prefix."""
        if not sheet_number:
            return SheetCategory.UNKNOWN

        prefix = sheet_number[0].upper()

        category_map = {
            'G': SheetCategory.GENERAL,
            'C': SheetCategory.CIVIL,
            'L': SheetCategory.LANDSCAPE,
            'S': SheetCategory.STRUCTURAL,
            'A': SheetCategory.ARCHITECTURAL,
            'I': SheetCategory.INTERIORS,
            'Q': SheetCategory.EQUIPMENT,
            'F': SheetCategory.FIRE_PROTECTION,
            'P': SheetCategory.PLUMBING,
            'M': SheetCategory.MECHANICAL,
            'E': SheetCategory.ELECTRICAL,
        }

        return category_map.get(prefix, SheetCategory.UNKNOWN)

    def _calculate_relevance(
        self,
        sheet_number: str,
        sheet_title: str,
        text_lower: str,
        category: SheetCategory
    ) -> Tuple[float, List[str]]:
        """Calculate roof relevance score for a page."""
        score = 0.0
        reasons = []

        # Check sheet number patterns
        for pattern in ROOF_SHEET_PATTERNS:
            if re.search(pattern, sheet_number, re.IGNORECASE):
                score += 0.5
                reasons.append(f"Sheet number matches roof pattern: {sheet_number}")
                break

        # Check if explicitly excluded
        for pattern in EXCLUDE_SHEET_PATTERNS:
            if re.search(pattern, sheet_number, re.IGNORECASE):
                # Don't fully exclude, but reduce score
                score -= 0.2
                break

        # Check sheet title
        if any(kw in sheet_title.lower() for kw in ['roof', 'roofing']):
            score += 0.4
            reasons.append(f"Title contains roof reference: {sheet_title}")

        # Check keywords in text
        keyword_score = 0.0
        matched_keywords = []

        for keyword, weight in ROOF_KEYWORDS.items():
            if keyword in text_lower:
                keyword_score += weight * 0.1  # Scale down keyword contribution
                matched_keywords.append(keyword)

        if keyword_score > 0:
            score += min(keyword_score, 0.4)  # Cap keyword contribution
            if matched_keywords:
                reasons.append(f"Keywords found: {', '.join(matched_keywords[:5])}")

        # Bonus for priority categories
        if category in PRIORITY_CATEGORIES:
            score += 0.1

        # Normalize to 0-1
        score = max(0, min(1, score))

        return round(score, 2), reasons

    def get_summary(self) -> Dict:
        """Get analysis summary."""
        return {
            'stats': self.stats,
            'filtered_sheets': [s.to_dict() for s in self.filtered_sheets],
            'filter_efficiency': f"{100 - (self.stats['roof_related_pages']/max(1, self.stats['pages_analyzed'])*100):.1f}%"
        }

    def export_filtered_pages(self, output_dir: str) -> List[str]:
        """Export filtered pages as individual PDFs or images for AI analysis."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        exported_files = []

        if not PDF2IMAGE_AVAILABLE:
            logger.warning("pdf2image not available - cannot export page images")
            return exported_files

        for sheet in self.filtered_sheets:
            try:
                # Convert specific page to image
                images = convert_from_path(
                    self.pdf_path,
                    first_page=sheet.page_number,
                    last_page=sheet.page_number,
                    dpi=150  # Balance between quality and size
                )

                if images:
                    filename = f"{sheet.sheet_number}_page{sheet.page_number}.png"
                    filepath = output_path / filename
                    images[0].save(filepath, 'PNG')
                    exported_files.append(str(filepath))
                    logger.debug(f"Exported: {filename}")

            except Exception as e:
                logger.error(f"Error exporting page {sheet.page_number}: {e}")

        logger.info(f"Exported {len(exported_files)} page images to {output_dir}")
        return exported_files


# ============================================================================
# STAGE 2: AI VISION ANALYSIS
# ============================================================================

class AIVisionAnalyzer:
    """
    Uses AI vision (Claude/OpenAI) to analyze filtered drawing pages.
    Extracts roofing details that text extraction cannot capture.
    """

    ANALYSIS_PROMPT = """You are an expert architectural drawing analyst specializing in commercial roofing.

Analyze this architectural drawing page and extract ALL roofing-related information.

For ROOF PLANS, identify and count:
- Roof drains (RD symbols, usually circles with crosshairs)
- Scuppers (rectangular openings in parapets)
- Overflow drains/scuppers
- RTUs/Mechanical curbs (rectangles with equipment labels)
- Skylights
- Roof hatches
- Pipe penetrations
- Any other roof penetrations

For ROOF DETAILS, identify:
- Detail number and title
- Scale
- Materials shown (membrane type, insulation, cover board)
- Flashing types
- Edge conditions
- Attachment methods visible

Also note:
- Sheet number (from title block)
- Drawing title
- Any specification section references (like "07 52 00")
- Referenced detail numbers
- Roof areas/zones shown
- Slopes or drainage directions indicated

Return your analysis as JSON with this structure:
{
    "sheet_number": "string",
    "drawing_title": "string",
    "drawing_type": "ROOF PLAN" | "ROOF DETAIL" | "ROOF SECTION" | "OTHER",
    "elements": {
        "drains": {"count": int, "notes": "string"},
        "scuppers": {"count": int, "type": "primary|overflow|both", "notes": "string"},
        "rtus_curbs": {"count": int, "notes": "string"},
        "skylights": {"count": int, "notes": "string"},
        "hatches": {"count": int, "notes": "string"},
        "penetrations": {"count": int, "notes": "string"}
    },
    "materials": {
        "membrane": "string or null",
        "insulation": "string or null",
        "cover_board": "string or null",
        "vapor_barrier": "string or null"
    },
    "details": [
        {
            "detail_number": "string",
            "title": "string",
            "scale": "string",
            "description": "string"
        }
    ],
    "references": {
        "spec_sections": ["string"],
        "other_details": ["string"]
    },
    "roof_areas": ["string"],
    "notes": "string",
    "confidence": float between 0 and 1
}

Be thorough but only include information clearly visible in the drawing. If you cannot determine something, use null."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize AI analyzer.

        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Model to use for analysis
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.model = model
        self.client = None

        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        else:
            logger.warning("Anthropic client not available - AI analysis disabled")

    def analyze_image(self, image_path: str) -> Optional[Dict]:
        """
        Analyze a single drawing image using AI vision.

        Args:
            image_path: Path to the image file

        Returns:
            Parsed analysis result or None if failed
        """
        if not self.client:
            logger.error("AI client not initialized")
            return None

        try:
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = base64.standard_b64encode(f.read()).decode('utf-8')

            # Determine media type
            ext = Path(image_path).suffix.lower()
            media_type = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }.get(ext, 'image/png')

            # Call Claude API with vision
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": self.ANALYSIS_PROMPT
                            }
                        ]
                    }
                ]
            )

            # Parse response
            response_text = response.content[0].text

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                return json.loads(json_match.group())
            else:
                logger.warning(f"Could not parse JSON from response: {response_text[:200]}")
                return {"raw_response": response_text}

        except Exception as e:
            logger.error(f"Error analyzing image {image_path}: {e}")
            return None

    def analyze_batch(
        self,
        image_paths: List[str],
        max_concurrent: int = 3
    ) -> List[Tuple[str, Optional[Dict]]]:
        """
        Analyze multiple images concurrently.

        Args:
            image_paths: List of image file paths
            max_concurrent: Maximum concurrent API calls

        Returns:
            List of (image_path, analysis_result) tuples
        """
        results = []

        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            future_to_path = {
                executor.submit(self.analyze_image, path): path
                for path in image_paths
            }

            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    result = future.result()
                    results.append((path, result))
                    logger.info(f"Analyzed: {Path(path).name}")
                except Exception as e:
                    logger.error(f"Error processing {path}: {e}")
                    results.append((path, None))

        return results


# ============================================================================
# MAIN PARSER CLASS
# ============================================================================

class LargeDrawingSetParser:
    """
    Main parser for large architectural drawing sets.
    Combines filtering and AI analysis.
    """

    def __init__(
        self,
        pdf_path: str,
        api_key: Optional[str] = None,
        min_relevance_score: float = 0.3,
        use_ai_vision: bool = True
    ):
        """
        Initialize parser.

        Args:
            pdf_path: Path to the PDF file
            api_key: Optional API key for AI vision
            min_relevance_score: Minimum score for page to be considered relevant
            use_ai_vision: Whether to use AI vision analysis
        """
        self.pdf_path = pdf_path
        self.filter = DrawingSetFilter(pdf_path, min_relevance_score)
        self.ai_analyzer = AIVisionAnalyzer(api_key) if use_ai_vision else None
        self.results: Dict[str, Any] = {}

    def parse(
        self,
        max_pages: Optional[int] = None,
        analyze_with_ai: bool = True,
        output_dir: Optional[str] = None
    ) -> Dict:
        """
        Parse the drawing set.

        Args:
            max_pages: Optional page limit for testing
            analyze_with_ai: Whether to run AI analysis on filtered pages
            output_dir: Directory for exported images (temp dir if None)

        Returns:
            Complete parsing results
        """
        logger.info(f"Starting parse of: {self.pdf_path}")

        # Stage 1: Filter pages
        logger.info("STAGE 1: Filtering pages...")
        filtered_sheets = self.filter.analyze_pdf(max_pages)

        self.results = {
            'filename': Path(self.pdf_path).name,
            'stage1_filter': self.filter.get_summary(),
            'filtered_sheets': [s.to_dict() for s in filtered_sheets],
            'roof_details': [],
            'ai_analysis': []
        }

        # Stage 2: AI Vision Analysis
        if analyze_with_ai and self.ai_analyzer and self.ai_analyzer.client:
            logger.info("STAGE 2: AI Vision Analysis...")

            # Create temp directory for images if not specified
            if output_dir is None:
                output_dir = tempfile.mkdtemp(prefix='drawing_analysis_')

            # Export filtered pages as images
            image_paths = self.filter.export_filtered_pages(output_dir)

            if image_paths:
                # Analyze images
                ai_results = self.ai_analyzer.analyze_batch(image_paths)

                for image_path, analysis in ai_results:
                    if analysis:
                        self.results['ai_analysis'].append({
                            'image': Path(image_path).name,
                            'analysis': analysis
                        })

                        # Convert to RoofDetail objects
                        if isinstance(analysis, dict) and 'drawing_type' in analysis:
                            detail = self._convert_to_roof_detail(analysis, image_path)
                            if detail:
                                self.results['roof_details'].append(detail.to_dict())
            else:
                logger.warning("No images exported - skipping AI analysis")
        else:
            logger.info("AI analysis disabled or unavailable")

        # Generate summary
        self.results['summary'] = self._generate_summary()

        return self.results

    def _convert_to_roof_detail(self, analysis: Dict, image_path: str) -> Optional[RoofDetail]:
        """Convert AI analysis to RoofDetail object."""
        try:
            # Extract page number from filename
            filename = Path(image_path).stem
            page_match = re.search(r'page(\d+)', filename)
            page_num = int(page_match.group(1)) if page_match else 0

            elements = analysis.get('elements', {})

            return RoofDetail(
                sheet_number=analysis.get('sheet_number', ''),
                page_number=page_num,
                detail_type=analysis.get('drawing_type', 'UNKNOWN'),
                title=analysis.get('drawing_title', ''),
                drains=elements.get('drains', {}).get('count', 0),
                scuppers=elements.get('scuppers', {}).get('count', 0),
                rtus=elements.get('rtus_curbs', {}).get('count', 0),
                penetrations=elements.get('penetrations', {}).get('count', 0),
                skylights=elements.get('skylights', {}).get('count', 0),
                hatches=elements.get('hatches', {}).get('count', 0),
                membrane_type=analysis.get('materials', {}).get('membrane', ''),
                insulation_type=analysis.get('materials', {}).get('insulation', ''),
                detail_references=analysis.get('references', {}).get('other_details', []),
                spec_references=analysis.get('references', {}).get('spec_sections', []),
                ai_description=analysis.get('notes', ''),
                ai_confidence=analysis.get('confidence', 0.0)
            )
        except Exception as e:
            logger.error(f"Error converting analysis to RoofDetail: {e}")
            return None

    def _generate_summary(self) -> Dict:
        """Generate summary of findings."""
        total_drains = sum(d.get('drains', 0) for d in self.results.get('roof_details', []))
        total_scuppers = sum(d.get('scuppers', 0) for d in self.results.get('roof_details', []))
        total_rtus = sum(d.get('rtus', 0) for d in self.results.get('roof_details', []))

        return {
            'total_pages_analyzed': self.results['stage1_filter']['stats']['pages_analyzed'],
            'roof_related_pages': self.results['stage1_filter']['stats']['roof_related_pages'],
            'filter_efficiency': self.results['stage1_filter']['filter_efficiency'],
            'roof_plans_found': sum(1 for d in self.results.get('roof_details', []) if d.get('detail_type') == 'ROOF PLAN'),
            'roof_details_found': sum(1 for d in self.results.get('roof_details', []) if d.get('detail_type') == 'ROOF DETAIL'),
            'total_drains': total_drains,
            'total_scuppers': total_scuppers,
            'total_rtus': total_rtus,
            'ai_analyses_completed': len(self.results.get('ai_analysis', []))
        }


# ============================================================================
# STANDALONE USAGE
# ============================================================================

def parse_large_drawing_set(
    pdf_path: str,
    api_key: Optional[str] = None,
    min_relevance: float = 0.3,
    use_ai: bool = True,
    max_pages: Optional[int] = None
) -> Dict:
    """
    Convenience function for parsing a large drawing set.

    Args:
        pdf_path: Path to PDF
        api_key: Anthropic API key
        min_relevance: Minimum relevance score for filtering
        use_ai: Whether to use AI vision
        max_pages: Optional page limit

    Returns:
        Parsing results dictionary
    """
    parser = LargeDrawingSetParser(
        pdf_path=pdf_path,
        api_key=api_key,
        min_relevance_score=min_relevance,
        use_ai_vision=use_ai
    )
    return parser.parse(max_pages=max_pages)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python large_drawing_set_parser.py <pdf_path> [max_pages]")
        print("\nExample:")
        print("  python large_drawing_set_parser.py drawings.pdf")
        print("  python large_drawing_set_parser.py drawings.pdf 100  # Test with first 100 pages")
        sys.exit(1)

    pdf_path = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else None

    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    use_ai = api_key is not None

    if not use_ai:
        print("Note: ANTHROPIC_API_KEY not set - running filter-only mode")
        print("Set the environment variable to enable AI vision analysis")

    print(f"\nParsing: {pdf_path}")
    print(f"Max pages: {max_pages or 'all'}")
    print(f"AI analysis: {'enabled' if use_ai else 'disabled'}")
    print("-" * 60)

    results = parse_large_drawing_set(
        pdf_path=pdf_path,
        api_key=api_key,
        use_ai=use_ai,
        max_pages=max_pages
    )

    # Print summary
    print("\n" + "=" * 60)
    print("PARSING RESULTS")
    print("=" * 60)

    summary = results.get('summary', {})
    print(f"\nTotal pages analyzed: {summary.get('total_pages_analyzed', 0)}")
    print(f"Roof-related pages found: {summary.get('roof_related_pages', 0)}")
    print(f"Filter efficiency: {summary.get('filter_efficiency', 'N/A')}")
    print(f"Roof plans: {summary.get('roof_plans_found', 0)}")
    print(f"Roof details: {summary.get('roof_details_found', 0)}")
    print(f"Total drains: {summary.get('total_drains', 0)}")
    print(f"Total scuppers: {summary.get('total_scuppers', 0)}")
    print(f"Total RTUs: {summary.get('total_rtus', 0)}")
    print(f"AI analyses: {summary.get('ai_analyses_completed', 0)}")

    # Print filtered sheets
    print("\nFiltered Sheets:")
    for sheet in results.get('filtered_sheets', [])[:20]:  # Show first 20
        print(f"  Page {sheet['page_number']}: {sheet['sheet_number']} - Score: {sheet['roof_relevance_score']}")
        if sheet.get('relevance_reasons'):
            for reason in sheet['relevance_reasons']:
                print(f"    - {reason}")

    # Save full results to JSON
    output_file = Path(pdf_path).stem + "_roof_analysis.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nFull results saved to: {output_file}")
