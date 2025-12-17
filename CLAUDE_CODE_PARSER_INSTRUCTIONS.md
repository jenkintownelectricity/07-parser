# Claude Code Instructions: Division 07 Drawing Parser Integration

> **For Claude Code AI Agent** | Lefebvre Design Solutions
> **Priority:** HIGH | **Type:** feat(tools)

---

## 1. OBJECTIVE

Build a tiered AI drawing parser that extracts Division 07 scope-specific information from architectural drawing PDFs for shop drawing creation.

**Processing Pipeline:**
```
PDF → Python/pdfplumber (Tier 1) → Groq Llama 3.3 70B (Tier 2) → Anthropic Claude (Tier 3)
       Extract & Classify            Analyze & Categorize           Deep Analysis & QA
```

---

## 2. DIRECTORY STRUCTURE

Create the following structure. **DO NOT deviate.**

```
tools/
└── parsers/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   ├── div07_scopes.py           # All Division 07 scope definitions
    │   └── drawing_types.py          # Drawing classification patterns
    ├── extractors/
    │   ├── __init__.py
    │   ├── pdf_extractor.py          # Tier 1: pdfplumber extraction
    │   └── text_processor.py         # Text cleaning and normalization
    ├── analyzers/
    │   ├── __init__.py
    │   ├── keyword_matcher.py        # Tier 1: Python keyword matching
    │   ├── groq_analyzer.py          # Tier 2: Groq Llama analysis
    │   └── claude_analyzer.py        # Tier 3: Anthropic deep analysis
    ├── models/
    │   ├── __init__.py
    │   └── schemas.py                # Pydantic models for data structures
    ├── outputs/
    │   ├── __init__.py
    │   ├── report_generator.py       # TXT/MD report generation
    │   ├── csv_exporter.py           # CSV for spreadsheet import
    │   └── json_exporter.py          # JSON for API/database
    ├── main.py                       # CLI entry point
    └── api.py                        # FastAPI router for backend integration

roofio-backend/
└── api/
    └── routes/
        └── parser.py                 # API endpoint integration

tests/
└── parsers/
    ├── __init__.py
    ├── test_pdf_extractor.py
    ├── test_keyword_matcher.py
    ├── test_groq_analyzer.py
    └── test_integration.py

docs/
└── PARSER.md                         # Full documentation
```

---

## 3. COMMIT SEQUENCE

Execute these commits IN ORDER. Each commit = ONE logical unit.

```bash
# Commit 1: Configuration modules
git add tools/parsers/config/
git commit -m "feat(parsers): Add Division 07 scope definitions and drawing type patterns"

# Commit 2: Tier 1 extractors
git add tools/parsers/extractors/
git commit -m "feat(parsers): Add PDF extraction with pdfplumber and text processing"

# Commit 3: Data models
git add tools/parsers/models/
git commit -m "feat(parsers): Add Pydantic schemas for parser data structures"

# Commit 4: Tier 1 analyzer
git add tools/parsers/analyzers/keyword_matcher.py
git commit -m "feat(parsers): Add Python keyword matching analyzer (Tier 1)"

# Commit 5: Tier 2 analyzer
git add tools/parsers/analyzers/groq_analyzer.py
git commit -m "feat(parsers): Add Groq Llama 3.3 70B analyzer (Tier 2)"

# Commit 6: Tier 3 analyzer
git add tools/parsers/analyzers/claude_analyzer.py
git commit -m "feat(parsers): Add Anthropic Claude deep analyzer (Tier 3)"

# Commit 7: Output generators
git add tools/parsers/outputs/
git commit -m "feat(parsers): Add report, CSV, and JSON output generators"

# Commit 8: CLI and API
git add tools/parsers/main.py tools/parsers/api.py
git commit -m "feat(parsers): Add CLI entry point and FastAPI router"

# Commit 9: Backend integration
git add roofio-backend/api/routes/parser.py
git commit -m "feat(backend): Integrate parser API endpoint with agency_id multi-tenancy"

# Commit 10: Tests
git add tests/parsers/
git commit -m "test(parsers): Add unit and integration tests for drawing parser"

# Commit 11: Documentation
git add docs/PARSER.md
git commit -m "docs(parsers): Add comprehensive parser documentation"

# Commit 12: Dependencies
git commit -m "chore(deps): Add pdfplumber, groq, anthropic to requirements.txt"
```

---

## 4. FILE CONTENTS

### 4.1. `tools/parsers/config/div07_scopes.py`

```python
"""
Division 07 Scope Definitions
Thermal and Moisture Protection

Each scope includes:
- Subsections with CSI numbers
- Keywords for text matching
- Common products/manufacturers
- Shop drawing requirements
"""

from typing import Dict, List, Any

DIV07_SCOPES: Dict[str, Dict[str, Any]] = {
    "071000": {
        "name": "Dampproofing and Waterproofing",
        "short": "WP",
        "description": "Below-grade waterproofing systems including sheet, fluid-applied, and cementitious",
        "subsections": {
            "071300": "Sheet Waterproofing",
            "071326": "Self-Adhering Sheet Waterproofing",
            "071353": "Elastomeric Sheet Waterproofing",
            "071400": "Fluid-Applied Waterproofing",
            "071413": "Hot Rubberized Asphalt Waterproofing",
            "071416": "Cold Fluid-Applied Waterproofing",
            "071600": "Cementitious and Reactive Waterproofing",
            "071616": "Crystalline Waterproofing",
            "071800": "Traffic Coatings",
            "071816": "Vehicular Traffic Coatings",
        },
        "keywords": [
            # Direct terms
            "waterproof", "water-proof", "waterproofing", "wp", "w.p.", "w/p",
            "dampproof", "damp-proof", "dampproofing",
            # Locations
            "below grade", "below-grade", "foundation wall", "foundation",
            "elevator pit", "elev pit", "elev. pit", "elevator shaft",
            "sump pit", "sump", "retaining wall", "basement", "cellar",
            "underslab", "under-slab", "under slab", "mud slab",
            "plaza deck", "podium", "podium deck", "parking deck",
            "tunnel", "vault", "mechanical pit",
            # Products/Systems
            "bituthene", "preprufe", "mel-rol", "rub-r-wall", "tuff-n-dri",
            "hydroduct", "protection board", "drainage board", "drain mat",
            "bentonite", "voltex", "cetco", "mirafi",
            "hot rubberized asphalt", "hra", "hot fluid applied",
            "cold applied", "fluid applied membrane",
            "crystalline", "xypex", "krystol", "penetron",
            "traffic coating", "traffic topping", "vehicular",
            # Spec references
            "071300", "071326", "071353", "071400", "071413", "071416", 
            "071600", "071616", "071800", "071816",
        ],
        "manufacturers": [
            "GCP Applied Technologies", "Carlisle", "Henry", "Tremco",
            "Sika", "BASF", "Cetco", "W.R. Meadows", "Polyguard",
        ],
        "shop_drawing_requirements": {
            "plans": "Foundation plans showing WP extent, drains, sumps",
            "sections": "Wall sections at grade transitions, elevator pits",
            "details": "Terminations, penetrations, inside/outside corners, tie-ins",
            "schedules": "Product schedule with coverage rates",
        },
    },
    
    "072000": {
        "name": "Thermal Protection",
        "short": "INSUL",
        "description": "Insulation and air/vapor barrier systems",
        "subsections": {
            "072100": "Thermal Insulation",
            "072119": "Foamed-In-Place Insulation",
            "072126": "Blown Insulation",
            "072129": "Sprayed Insulation",
            "072200": "Roof and Deck Insulation",
            "072300": "Exterior Insulation",
            "072400": "Exterior Insulation and Finish Systems",
            "072500": "Weather Barriers",
            "072700": "Air Barriers",
            "072713": "Self-Adhered Sheet Air Barriers",
            "072719": "Fluid-Applied Air Barriers",
            "072726": "Aerosol Air Sealing",
        },
        "keywords": [
            # Insulation
            "insulation", "thermal", "r-value", "u-value",
            "rigid insulation", "board insulation", "batt insulation",
            "spray foam", "spf", "closed cell", "open cell", "ccspf", "ocspf",
            "polyiso", "polyisocyanurate", "iso board",
            "xps", "extruded polystyrene", "styrofoam",
            "eps", "expanded polystyrene", "molded polystyrene",
            "mineral wool", "rockwool", "stone wool", "slag wool",
            "fiberglass", "glass fiber", "blown insulation",
            "continuous insulation", "ci", "c.i.",
            # Air/Vapor Barriers
            "air barrier", "air-barrier", "airbarrier", "ab",
            "vapor barrier", "vapor-barrier", "vapour barrier", "vb",
            "vapor retarder", "vapour retarder",
            "avb", "a.v.b.", "a/v barrier", "air and vapor",
            "weather barrier", "wrb", "water resistive barrier",
            "building wrap", "house wrap", "tyvek", "typar",
            # Products
            "perm-a-barrier", "permbarrier", "vps30", "vps 30",
            "blueskin", "prosoco", "r-guard", "air-shield",
            "henry", "carlisle", "tremco", "siga", "pro clima",
            "aerobarrier", "aeroseal",
            # EIFS
            "eifs", "exterior insulation finish", "synthetic stucco",
            "dryvit", "sto", "parex", "finestone",
            # Spec references
            "072100", "072119", "072200", "072400", "072500", 
            "072700", "072713", "072719", "072726",
        ],
        "manufacturers": [
            "GCP Applied Technologies", "Carlisle", "Henry", "Tremco",
            "Prosoco", "Siga", "Pro Clima", "Dryvit", "Sto",
            "Owens Corning", "Johns Manville", "Rockwool",
        ],
        "shop_drawing_requirements": {
            "plans": "Floor plans showing AB/VB extent by wall type",
            "elevations": "Building elevations showing barrier extent",
            "sections": "Wall sections with full assembly",
            "details": "Window/door jambs, heads, sills, penetrations, corners, transitions",
            "schedules": "Wall type schedule with barrier requirements",
        },
    },
    
    "073000": {
        "name": "Steep Slope Roofing",
        "short": "STEEP",
        "description": "Shingles, tiles, slate, and steep slope metal roofing",
        "subsections": {
            "073100": "Shingles and Shakes",
            "073113": "Asphalt Shingles",
            "073116": "Metal Shingles",
            "073119": "Slate Shingles",
            "073123": "Wood Shingles and Shakes",
            "073126": "Slate Roofing",
            "073129": "Wood Shingles and Shakes",
            "073200": "Roof Tiles",
            "073213": "Clay Roof Tiles",
            "073216": "Concrete Roof Tiles",
            "073400": "Manufactured Roofing",
            "073500": "Composite Roofing",
        },
        "keywords": [
            "shingle", "asphalt shingle", "architectural shingle", "3-tab",
            "slate", "slate roof", "slate shingle", "natural slate",
            "wood shake", "cedar shake", "wood shingle", "cedar shingle",
            "roof tile", "clay tile", "concrete tile", "terracotta",
            "metal shingle", "stone coated", "standing seam steep",
            "steep slope", "pitched roof", "gable", "hip roof",
            "ridge", "hip", "valley", "rake", "eave", "dormer",
            "underlayment", "ice dam", "ice & water", "ice and water shield",
            "starter strip", "drip edge", "rake edge",
            "073100", "073113", "073119", "073126", "073200", "073213", "073216",
        ],
        "manufacturers": [
            "GAF", "CertainTeed", "Owens Corning", "IKO", "Tamko",
            "Boral", "Ludowici", "US Tile", "DaVinci", "EcoStar",
        ],
        "shop_drawing_requirements": {
            "plans": "Roof plan with slopes, valleys, ridges",
            "elevations": "All elevations showing roof lines",
            "details": "Ridge, hip, valley, eave, rake, penetrations, dormers",
            "schedules": "Roofing material schedule",
        },
    },
    
    "074000": {
        "name": "Roofing and Siding Panels",
        "short": "PANEL",
        "description": "Metal panels, insulated panels, composite panels, siding",
        "subsections": {
            "074100": "Roof Panels",
            "074113": "Metal Roof Panels",
            "074116": "Insulated Metal Roof Panels",
            "074200": "Wall Panels",
            "074213": "Metal Wall Panels",
            "074216": "Insulated Metal Wall Panels",
            "074220": "Insulated Metal Panels",
            "074243": "Composite Wall Panels",
            "074246": "Fiber Cement Panels",
            "074300": "Siding",
            "074313": "Metal Siding",
            "074316": "Aluminum Siding",
            "074323": "Wood Siding",
            "074346": "Fiber Cement Siding",
            "074600": "Soffits",
            "074633": "Metal Soffits",
        },
        "keywords": [
            "metal panel", "wall panel", "roof panel",
            "standing seam", "snap lock", "mechanically seamed",
            "insulated metal panel", "imp", "foam core panel",
            "composite panel", "acm", "aluminum composite",
            "fiber cement", "hardie", "hardiepanel", "cementitious panel",
            "metal siding", "lap siding", "board and batten",
            "corrugated", "ribbed panel", "concealed fastener",
            "exposed fastener", "through fastened",
            "soffit", "fascia", "coping", "gravel stop",
            "centria", "metl-span", "kingspan", "berridge", "pac-clad",
            "mbci", "petersen", "atas", "morin",
            "074100", "074113", "074200", "074213", "074216", "074243", "074246",
        ],
        "manufacturers": [
            "Centria", "Metl-Span", "Kingspan", "Berridge", "Pac-Clad",
            "MBCI", "Petersen Aluminum", "ATAS", "Morin", "Metal Sales",
            "James Hardie", "Nichiha", "Cembrit",
        ],
        "shop_drawing_requirements": {
            "plans": "Panel layout plans with dimensions",
            "elevations": "Panel elevations with joint layout",
            "sections": "Panel sections at openings, corners, base, head",
            "details": "Joints, corners, penetrations, flashings, trim",
            "schedules": "Panel schedule with types, finishes, gauges",
        },
    },
    
    "075000": {
        "name": "Membrane Roofing",
        "short": "MEMB",
        "description": "Single-ply, built-up, modified bitumen, and fluid-applied roofing",
        "subsections": {
            "075100": "Built-Up Roofing",
            "075113": "Asphalt Built-Up Roofing",
            "075116": "Coal-Tar Built-Up Roofing",
            "075200": "Modified Bituminous Membrane Roofing",
            "075213": "Atactic Polypropylene (APP) Roofing",
            "075216": "Styrene-Butadiene-Styrene (SBS) Roofing",
            "075300": "Elastomeric Membrane Roofing",
            "075323": "EPDM Roofing",
            "075400": "Thermoplastic Membrane Roofing",
            "075413": "KEE Roofing",
            "075416": "TPO Roofing",
            "075419": "PVC Roofing",
            "075500": "Protected Membrane Roofing",
            "075600": "Fluid-Applied Roofing",
            "075700": "Coated Foamed Roofing",
            "075800": "Roll Roofing",
        },
        "keywords": [
            "membrane", "roofing membrane", "single ply", "single-ply",
            "built-up", "bur", "built up roof", "hot mopped", "cold process",
            "modified bitumen", "mod bit", "modbit",
            "app", "atactic polypropylene", "torch applied", "torch down",
            "sbs", "styrene butadiene", "cold adhesive", "self-adhered",
            "epdm", "rubber roof", "ethylene propylene",
            "tpo", "thermoplastic polyolefin", "thermoplastic olefin",
            "pvc", "polyvinyl chloride", "vinyl membrane",
            "kee", "ketone ethylene ester",
            "protected membrane", "pmr", "irma", "inverted roof",
            "ballasted", "mechanically attached", "fully adhered",
            "fluid applied roof", "silicone roof", "coating",
            "sarnafil", "sika", "firestone", "carlisle", "gaf", "johns manville",
            "versico", "tremco", "soprema", "iko", "polyglass",
            "075100", "075200", "075216", "075300", "075323", 
            "075400", "075416", "075419", "075500", "075600",
        ],
        "manufacturers": [
            "Sika Sarnafil", "Firestone", "Carlisle", "GAF", "Johns Manville",
            "Versico", "Tremco", "Soprema", "IKO", "Polyglass", "Elevate",
        ],
        "shop_drawing_requirements": {
            "plans": "Roof plan with drains, slopes, equipment, penetrations",
            "details": "Drains, curbs, penetrations, edges, corners, expansion joints",
            "sections": "Roof sections at parapets, equipment, transitions",
            "schedules": "Roofing schedule with assemblies, R-values",
        },
    },
    
    "076000": {
        "name": "Flashing and Sheet Metal",
        "short": "FLASH",
        "description": "Sheet metal flashing, trim, and cladding",
        "subsections": {
            "076100": "Sheet Metal Roofing",
            "076200": "Sheet Metal Flashing and Trim",
            "076213": "Stainless Steel Flashing",
            "076216": "Copper Flashing",
            "076219": "Lead Flashing",
            "076220": "Manufactured Flashing and Trim",
            "076300": "Sheet Metal Roofing Specialties",
            "076400": "Sheet Metal Wall Cladding",
            "076500": "Flexible Flashing",
            "076513": "Laminated Sheet Flashing",
            "076516": "Self-Adhering Flashing",
        },
        "keywords": [
            "flashing", "sheet metal", "metal flashing", "sm flashing",
            "counterflashing", "counter flashing", "counter-flashing",
            "base flashing", "cap flashing", "step flashing",
            "through-wall flashing", "twf", "through wall",
            "copper", "stainless", "stainless steel", "galvanized",
            "lead coated copper", "freedom gray", "kynar", "pvdf",
            "reglet", "surface reglet", "receiver", "receiver channel",
            "termination bar", "term bar", "cleat", "cleats",
            "drip edge", "gravel stop", "fascia", "coping", "cap",
            "expansion joint", "control joint", "metal coping",
            "roof edge", "parapet cap", "parapet coping",
            "curb flashing", "pitch pan", "pitch pocket",
            "scupper", "overflow scupper", "conductor head", "leader head",
            "076100", "076200", "076213", "076216", "076500", "076513",
        ],
        "manufacturers": [
            "Metal Era", "Hickman", "Tremco", "Carlisle", "Firestone",
            "Revere Copper", "Petersen Aluminum", "Pac-Clad",
        ],
        "shop_drawing_requirements": {
            "plans": "Roof plan with flashing locations",
            "elevations": "Elevations showing flashing at all conditions",
            "details": "Each flashing type, joints, corners, terminations",
            "sections": "Wall sections at all flashing conditions",
        },
    },
    
    "077000": {
        "name": "Roof and Wall Specialties and Accessories",
        "short": "SPEC",
        "description": "Roof accessories, specialties, pavers, green roofs",
        "subsections": {
            "077100": "Roof Specialties",
            "077123": "Manufactured Gutters",
            "077126": "Manufactured Downspouts",
            "077129": "Manufactured Roof Expansion Joints",
            "077133": "Roof Hatches",
            "077136": "Roof Smoke Vents",
            "077200": "Roof Accessories",
            "077213": "Roof Hatches",
            "077216": "Roof Smoke Vents",
            "077223": "Roof Walk Systems",
            "077226": "Roof Walkway Pads",
            "077253": "Snow Guards",
            "077263": "Roof Walkways",
            "077300": "Roof-Mounted Equipment Supports",
            "077600": "Roof Pavers",
            "077700": "Wall Specialties",
            "077800": "Green Roof Systems",
        },
        "keywords": [
            "roof hatch", "roof access", "smoke vent", "smoke hatch",
            "skylight", "unit skylight", "curb mounted",
            "curb", "roof curb", "equipment curb", "mechanical curb",
            "gutter", "downspout", "leader", "scupper", "conductor",
            "expansion joint", "roof expansion joint", "seismic joint",
            "roof drain", "overflow drain", "internal drain", "siphonic",
            "snow guard", "snow fence", "snow retention", "ice retention",
            "roof walkway", "walkpad", "walk pad", "protection mat",
            "roof paver", "pedestal paver", "concrete paver", "porcelain paver",
            "green roof", "vegetative roof", "vegetated roof",
            "extensive green", "intensive green", "roof garden",
            "equipment support", "pipe support", "conduit support",
            "bilco", "milcor", "nystrom", "babcock davis",
            "077100", "077123", "077133", "077200", "077253", "077263", 
            "077300", "077600", "077800",
        ],
        "manufacturers": [
            "Bilco", "Milcor", "Nystrom", "Babcock Davis", "Acudor",
            "Bison", "Archatrak", "Hanover", "Wausau",
            "S&P USA", "GreenGrid", "American Hydrotech", "LiveRoof",
        ],
        "shop_drawing_requirements": {
            "plans": "Roof plan with accessory locations",
            "elevations": "Equipment elevations",
            "details": "Each accessory type, curbs, supports, flashings",
            "schedules": "Accessory schedule with types and sizes",
        },
    },
    
    "078000": {
        "name": "Fire and Smoke Protection",
        "short": "FIRE",
        "description": "Fireproofing and firestopping systems",
        "subsections": {
            "078100": "Applied Fireproofing",
            "078110": "Cementitious Fireproofing",
            "078113": "Intumescent Fireproofing",
            "078120": "Magnesium Oxychloride Fireproofing",
            "078200": "Board Fireproofing",
            "078400": "Firestopping",
            "078413": "Penetration Firestopping",
            "078443": "Joint Firestopping",
            "078446": "Fire-Resistive Joint Systems",
        },
        "keywords": [
            "fireproof", "fire proof", "fire-proof", "fireproofing",
            "sfrm", "spray fireproofing", "spray applied fireproofing",
            "intumescent", "intumescent coating", "thin film",
            "cementitious fireproofing", "cafco", "isolatek",
            "firestop", "fire stop", "fire-stop", "firestopping",
            "penetration seal", "through penetration", "membrane penetration",
            "fire barrier", "fire wall", "fire partition",
            "fire rated", "hourly rating", "ul listing",
            "smoke seal", "smoke barrier", "smoke partition",
            "ul listed", "fire rating", "1-hour", "2-hour", "3-hour",
            "hilti", "specified technologies", "sti", "3m", "tremco",
            "078100", "078110", "078113", "078400", "078413", "078443",
        ],
        "manufacturers": [
            "Hilti", "STI (Specified Technologies)", "3M", "Tremco",
            "Isolatek", "Cafco", "PPG", "Carboline", "Nullifire",
        ],
        "shop_drawing_requirements": {
            "plans": "Floor plans with fire-rated assemblies",
            "elevations": "Fire barrier locations",
            "details": "Each penetration type, joint conditions",
            "schedules": "Firestop schedule with UL numbers",
        },
    },
    
    "079000": {
        "name": "Joint Protection",
        "short": "SEAL",
        "description": "Joint sealants and expansion joint covers",
        "subsections": {
            "079100": "Joint Fillers",
            "079200": "Joint Sealants",
            "079213": "Elastomeric Joint Sealants",
            "079219": "Acoustical Joint Sealants",
            "079500": "Expansion Control",
            "079513": "Expansion Joint Cover Assemblies",
            "079516": "Exterior Expansion Joint Cover Assemblies",
            "079519": "Interior Expansion Joint Cover Assemblies",
        },
        "keywords": [
            "sealant", "joint sealant", "caulk", "caulking",
            "silicone", "silicone sealant", "neutral cure", "acetoxy",
            "polyurethane", "urethane sealant", "pu sealant",
            "polysulfide", "hybrid", "ms polymer", "smp",
            "expansion joint", "control joint", "movement joint",
            "seismic joint", "building separation",
            "backer rod", "bond breaker", "joint filler", "foam rod",
            "weatherseal", "weather seal", "perimeter seal",
            "curtain wall seal", "glazing seal", "sssg",
            "dow corning", "momentive", "tremco", "pecora",
            "sika", "basf", "bostik",
            "079100", "079200", "079213", "079500", "079513",
        ],
        "manufacturers": [
            "Dow", "Momentive", "Tremco", "Pecora", "Sika", "BASF", "Bostik",
            "Inpro", "Balco", "Construction Specialties", "Emseal",
        ],
        "shop_drawing_requirements": {
            "plans": "Plans with joint locations",
            "elevations": "Elevations with expansion joints",
            "details": "Each joint type and sealant application",
            "schedules": "Sealant schedule with types and colors",
        },
    },
}


def get_scope(scope_id: str) -> Dict[str, Any]:
    """Get scope configuration by ID."""
    return DIV07_SCOPES.get(scope_id, {})


def get_all_keywords(scope_id: str) -> List[str]:
    """Get all keywords for a scope including subsection numbers."""
    scope = get_scope(scope_id)
    if not scope:
        return []
    return scope.get("keywords", [])


def get_scope_by_keyword(keyword: str) -> List[str]:
    """Find which scopes contain a keyword."""
    matching_scopes = []
    keyword_lower = keyword.lower()
    for scope_id, scope in DIV07_SCOPES.items():
        for kw in scope.get("keywords", []):
            if kw.lower() == keyword_lower or keyword_lower in kw.lower():
                matching_scopes.append(scope_id)
                break
    return matching_scopes
```

---

### 4.2. `tools/parsers/config/drawing_types.py`

```python
"""
Drawing Type Classification Patterns
For identifying sheet types in construction documents
"""

from typing import Dict, List, Any
import re

DRAWING_TYPES: Dict[str, Dict[str, Any]] = {
    "Cover/Index": {
        "patterns": [
            r"\bcover\b", r"\bindex\b", r"drawing list", r"sheet index",
            r"table of contents", r"\btoc\b", r"^g[-.]?0", r"^t[-.]?0"
        ],
        "priority": 0,
        "shop_drawing_relevance": "reference",
    },
    "General Notes": {
        "patterns": [
            r"general notes", r"abbreviations", r"symbols", r"legend",
            r"^g[-.]?[0-9]", r"keynotes"
        ],
        "priority": 1,
        "shop_drawing_relevance": "reference",
    },
    "Site Plan": {
        "patterns": [
            r"site plan", r"^c[-.]?[0-9]", r"^l[-.]?[0-9]",
            r"civil", r"grading", r"layout plan", r"site layout"
        ],
        "priority": 2,
        "shop_drawing_relevance": "context",
    },
    "Floor Plan": {
        "patterns": [
            r"floor plan", r"plan.*level", r"level.*plan",
            r"^a[-.]?1[0-9]", r"basement plan", r"ground floor",
            r"first floor", r"second floor", r"typical floor",
            r"mezzanine", r"penthouse"
        ],
        "priority": 3,
        "shop_drawing_relevance": "high",
    },
    "Roof Plan": {
        "patterns": [
            r"roof plan", r"roofing plan", r"roof drainage",
            r"roof framing", r"equipment plan.*roof"
        ],
        "priority": 3,
        "shop_drawing_relevance": "critical",
    },
    "Reflected Ceiling Plan": {
        "patterns": [
            r"reflected ceiling", r"rcp", r"ceiling plan",
            r"^a[-.]?2[0-9].*ceiling"
        ],
        "priority": 4,
        "shop_drawing_relevance": "low",
    },
    "Exterior Elevation": {
        "patterns": [
            r"exterior elevation", r"building elevation",
            r"^a[-.]?2[0-9]", r"north elev", r"south elev",
            r"east elev", r"west elev", r"elevation.*exterior"
        ],
        "priority": 5,
        "shop_drawing_relevance": "critical",
    },
    "Interior Elevation": {
        "patterns": [
            r"interior elevation", r"^a[-.]?6[0-9]", r"interior elev"
        ],
        "priority": 6,
        "shop_drawing_relevance": "low",
    },
    "Building Section": {
        "patterns": [
            r"building section", r"bldg section", r"^a[-.]?3[0-9]",
            r"longitudinal section", r"transverse section",
            r"cross section", r"section.*building"
        ],
        "priority": 7,
        "shop_drawing_relevance": "critical",
    },
    "Wall Section": {
        "patterns": [
            r"wall section", r"wall sect", r"^a[-.]?5[0-9]",
            r"typical wall", r"exterior wall section",
            r"curtain wall section", r"parapet section"
        ],
        "priority": 8,
        "shop_drawing_relevance": "critical",
    },
    "Enlarged Plan": {
        "patterns": [
            r"enlarged", r"blow.?up", r"partial plan",
            r"area plan", r"enlarged plan"
        ],
        "priority": 9,
        "shop_drawing_relevance": "high",
    },
    "Detail": {
        "patterns": [
            r"\bdetail\b", r"^a[-.]?[89][0-9]", r"typ\.?\s*det",
            r"typical det", r"standard det"
        ],
        "priority": 10,
        "shop_drawing_relevance": "critical",
    },
    "Schedule": {
        "patterns": [
            r"\bschedule\b", r"^a[-.]?0[0-9]", r"door schedule",
            r"window schedule", r"finish schedule", r"room finish"
        ],
        "priority": 11,
        "shop_drawing_relevance": "reference",
    },
    "Structural Foundation": {
        "patterns": [
            r"foundation", r"\bfdn\b", r"\bfndn\b", r"footing",
            r"^s[-.]?[12][0-9]", r"\bftg\b", r"pile", r"caisson",
            r"mat foundation", r"spread footing", r"grade beam"
        ],
        "priority": 12,
        "shop_drawing_relevance": "critical",  # For WP scope
    },
    "Structural Framing": {
        "patterns": [
            r"framing", r"^s[-.]?[3-9][0-9]", r"structural",
            r"steel framing", r"roof framing", r"floor framing"
        ],
        "priority": 13,
        "shop_drawing_relevance": "high",
    },
    "Mechanical": {
        "patterns": [
            r"mechanical", r"^m[-.]?[0-9]", r"\bhvac\b",
            r"ductwork", r"piping", r"equipment"
        ],
        "priority": 14,
        "shop_drawing_relevance": "reference",
    },
    "Electrical": {
        "patterns": [
            r"electrical", r"^e[-.]?[0-9]", r"lighting",
            r"power", r"panel schedule"
        ],
        "priority": 15,
        "shop_drawing_relevance": "reference",
    },
    "Plumbing": {
        "patterns": [
            r"plumbing", r"^p[-.]?[0-9]", r"piping",
            r"drainage", r"sanitary", r"storm"
        ],
        "priority": 16,
        "shop_drawing_relevance": "reference",
    },
}


def classify_drawing(text: str, sheet_number: str = "") -> str:
    """
    Classify a drawing based on its content and sheet number.
    Returns the drawing type with highest confidence.
    """
    text_lower = text.lower()
    sheet_lower = sheet_number.lower()
    
    matches = []
    
    for dtype, config in DRAWING_TYPES.items():
        for pattern in config["patterns"]:
            if re.search(pattern, text_lower, re.IGNORECASE) or \
               re.search(pattern, sheet_lower, re.IGNORECASE):
                matches.append((dtype, config["priority"]))
                break
    
    if not matches:
        return "Other"
    
    # Return lowest priority number (most specific match)
    matches.sort(key=lambda x: x[1])
    return matches[0][0]


def get_relevance(drawing_type: str) -> str:
    """Get shop drawing relevance level for a drawing type."""
    config = DRAWING_TYPES.get(drawing_type, {})
    return config.get("shop_drawing_relevance", "low")


def get_critical_types() -> List[str]:
    """Get list of drawing types critical for shop drawings."""
    return [
        dtype for dtype, config in DRAWING_TYPES.items()
        if config.get("shop_drawing_relevance") == "critical"
    ]
```

---

### 4.3. `tools/parsers/models/schemas.py`

```python
"""
Pydantic Models for Drawing Parser
Data validation and serialization
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
from uuid import UUID


class AnalysisTier(str, Enum):
    PYTHON = "python"
    GROQ = "groq"
    ANTHROPIC = "anthropic"


class DrawingType(str, Enum):
    COVER = "Cover/Index"
    GENERAL_NOTES = "General Notes"
    SITE_PLAN = "Site Plan"
    FLOOR_PLAN = "Floor Plan"
    ROOF_PLAN = "Roof Plan"
    EXTERIOR_ELEVATION = "Exterior Elevation"
    INTERIOR_ELEVATION = "Interior Elevation"
    BUILDING_SECTION = "Building Section"
    WALL_SECTION = "Wall Section"
    ENLARGED_PLAN = "Enlarged Plan"
    DETAIL = "Detail"
    SCHEDULE = "Schedule"
    STRUCTURAL_FOUNDATION = "Structural Foundation"
    STRUCTURAL_FRAMING = "Structural Framing"
    MECHANICAL = "Mechanical"
    ELECTRICAL = "Electrical"
    PLUMBING = "Plumbing"
    OTHER = "Other"


class Relevance(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    REFERENCE = "reference"
    CONTEXT = "context"
    LOW = "low"


class PageExtraction(BaseModel):
    """Raw extraction from a single PDF page."""
    page_number: int
    sheet_number: Optional[str] = None
    sheet_title: Optional[str] = None
    raw_text: str
    text_preview: str = Field(max_length=500)
    word_count: int
    extraction_timestamp: datetime = Field(default_factory=datetime.utcnow)


class PageClassification(BaseModel):
    """Classification results for a page."""
    page_number: int
    sheet_number: Optional[str] = None
    drawing_type: DrawingType
    relevance: Relevance
    confidence: float = Field(ge=0.0, le=1.0)
    classified_by: AnalysisTier


class ScopeMatch(BaseModel):
    """Match result for a specific scope."""
    scope_id: str
    scope_name: str
    page_number: int
    sheet_number: Optional[str] = None
    drawing_type: DrawingType
    matched_keywords: List[str]
    relevance_score: float = Field(ge=0.0, le=1.0)
    notes: Optional[str] = None


class ScopeAnalysis(BaseModel):
    """Complete analysis for a single scope."""
    scope_id: str
    scope_name: str
    short_code: str
    total_sheets: int
    sheets_by_type: Dict[str, int]
    matched_pages: List[ScopeMatch]
    critical_sheets: List[ScopeMatch]
    shop_drawing_estimate: Dict[str, Any]
    analysis_tier: AnalysisTier
    analysis_notes: Optional[str] = None


class GroqAnalysis(BaseModel):
    """Groq Llama analysis results."""
    scope_id: str
    page_number: int
    sheet_number: Optional[str] = None
    analysis_text: str
    identified_items: List[str]
    conditions: List[str]
    recommendations: List[str]
    confidence: float
    processing_time_ms: int


class ClaudeAnalysis(BaseModel):
    """Anthropic Claude deep analysis results."""
    scope_id: str
    page_numbers: List[int]
    comprehensive_analysis: str
    detail_inventory: Dict[str, int]
    special_conditions: List[str]
    coordination_items: List[str]
    shop_drawing_recommendations: List[str]
    estimated_shop_drawing_count: int
    processing_time_ms: int


class ParseResult(BaseModel):
    """Complete parse result for a document."""
    document_name: str
    document_path: str
    total_pages: int
    parse_timestamp: datetime = Field(default_factory=datetime.utcnow)
    selected_scopes: List[str]
    
    # Tier 1: Python extraction
    extractions: List[PageExtraction]
    classifications: List[PageClassification]
    
    # Tier 1: Keyword matching
    scope_analyses: Dict[str, ScopeAnalysis]
    
    # Tier 2: Groq analysis (optional)
    groq_analyses: Optional[List[GroqAnalysis]] = None
    
    # Tier 3: Claude analysis (optional)
    claude_analyses: Optional[List[ClaudeAnalysis]] = None
    
    # Summary
    executive_summary: Optional[str] = None
    total_relevant_sheets: int = 0
    processing_time_ms: int = 0


class ParserConfig(BaseModel):
    """Configuration for parser execution."""
    pdf_path: str
    selected_scopes: List[str]
    enable_groq: bool = True
    enable_claude: bool = True
    groq_batch_size: int = 10
    claude_batch_size: int = 20
    output_dir: str = "./output"
    output_formats: List[str] = ["txt", "csv", "json"]


# Database model for storing results
class ParseResultDB(BaseModel):
    """Database storage model with multi-tenancy."""
    id: Optional[UUID] = None
    agency_id: UUID  # Multi-tenant - REQUIRED
    project_id: Optional[UUID] = None
    document_name: str
    document_hash: str  # For deduplication
    parse_result: Dict[str, Any]  # JSON blob
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[UUID] = None
```

---

### 4.4. `tools/parsers/extractors/pdf_extractor.py`

```python
"""
Tier 1: PDF Text Extraction
Uses pdfplumber for reliable text extraction from construction drawings
"""

import pdfplumber
import re
import os
from typing import List, Generator, Optional
from datetime import datetime
import hashlib

from ..models.schemas import PageExtraction


class PDFExtractor:
    """
    Extract text content from PDF drawing sets.
    
    Optimized for construction documents which often have:
    - Title blocks with sheet numbers
    - Dense technical text
    - Tables and schedules
    - CAD-generated vector text
    """
    
    def __init__(self, pdf_path: str):
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        self.pdf_path = pdf_path
        self.file_name = os.path.basename(pdf_path)
        self.file_size = os.path.getsize(pdf_path)
        self.file_hash = self._compute_hash()
        self.total_pages = 0
        
    def _compute_hash(self) -> str:
        """Compute MD5 hash for deduplication."""
        hasher = hashlib.md5()
        with open(self.pdf_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def _extract_sheet_number(self, text: str) -> Optional[str]:
        """
        Extract sheet number from page text.
        Handles common formats: A1.01, A-101, S1, SK-1, etc.
        """
        patterns = [
            # Standard architectural: A1.01, A-1.01, A101
            r'([A-Z]{1,2}[-.]?\d{1,3}[A-Z]?(?:\.\d{1,2})?)',
            # Sketch numbers: SK-1, SK1
            r'(SK[-.]?\d+[A-Z]?)',
            # Sheet prefix: SHEET A1.01
            r'SHEET\s+([A-Z]?\d+(?:\.\d+)?)',
            # Drawing number in title block
            r'DWG\.?\s*(?:NO\.?)?\s*([A-Z]?\d+(?:\.\d+)?)',
        ]
        
        # Search in first 500 chars (title block area)
        search_area = text[:500] if len(text) > 500 else text
        
        for pattern in patterns:
            match = re.search(pattern, search_area, re.IGNORECASE)
            if match:
                return match.group(1).upper()
        
        return None
    
    def _extract_sheet_title(self, text: str) -> Optional[str]:
        """Extract sheet title from page text."""
        lines = text.split('\n')
        
        # Look for common title patterns in first 20 lines
        for line in lines[:20]:
            line = line.strip()
            # Skip very short or very long lines
            if len(line) < 5 or len(line) > 100:
                continue
            # Skip lines that are just numbers/dates
            if re.match(r'^[\d\s\-/\.]+$', line):
                continue
            # Skip sheet numbers
            if re.match(r'^[A-Z]{1,2}[-.]?\d', line):
                continue
            # Return first meaningful line
            if any(c.isalpha() for c in line):
                return line[:100]
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        if not text:
            return ""
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive special character sequences
        text = re.sub(r'[_\-=]{5,}', ' ', text)
        
        # Remove control characters
        text = ''.join(c for c in text if c.isprintable() or c in '\n\t')
        
        return text.strip()
    
    def extract_page(self, page_number: int) -> PageExtraction:
        """Extract content from a single page."""
        with pdfplumber.open(self.pdf_path) as pdf:
            if page_number < 1 or page_number > len(pdf.pages):
                raise ValueError(f"Invalid page number: {page_number}")
            
            page = pdf.pages[page_number - 1]
            raw_text = page.extract_text() or ""
            cleaned_text = self._clean_text(raw_text)
            
            return PageExtraction(
                page_number=page_number,
                sheet_number=self._extract_sheet_number(cleaned_text),
                sheet_title=self._extract_sheet_title(cleaned_text),
                raw_text=cleaned_text,
                text_preview=cleaned_text[:500] if cleaned_text else "",
                word_count=len(cleaned_text.split()),
                extraction_timestamp=datetime.utcnow(),
            )
    
    def extract_all(self, 
                    progress_callback=None) -> Generator[PageExtraction, None, None]:
        """
        Extract all pages as a generator.
        
        Args:
            progress_callback: Optional callback(current, total) for progress updates
            
        Yields:
            PageExtraction for each page
        """
        with pdfplumber.open(self.pdf_path) as pdf:
            self.total_pages = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages):
                page_num = i + 1
                
                if progress_callback:
                    progress_callback(page_num, self.total_pages)
                
                raw_text = page.extract_text() or ""
                cleaned_text = self._clean_text(raw_text)
                
                yield PageExtraction(
                    page_number=page_num,
                    sheet_number=self._extract_sheet_number(cleaned_text),
                    sheet_title=self._extract_sheet_title(cleaned_text),
                    raw_text=cleaned_text,
                    text_preview=cleaned_text[:500] if cleaned_text else "",
                    word_count=len(cleaned_text.split()),
                    extraction_timestamp=datetime.utcnow(),
                )
    
    def extract_all_list(self, progress_callback=None) -> List[PageExtraction]:
        """Extract all pages and return as list."""
        return list(self.extract_all(progress_callback))
    
    def get_metadata(self) -> dict:
        """Get PDF metadata."""
        with pdfplumber.open(self.pdf_path) as pdf:
            meta = pdf.metadata or {}
            return {
                "file_name": self.file_name,
                "file_path": self.pdf_path,
                "file_size_bytes": self.file_size,
                "file_hash": self.file_hash,
                "total_pages": len(pdf.pages),
                "title": meta.get("Title", ""),
                "author": meta.get("Author", ""),
                "creator": meta.get("Creator", ""),
                "created": meta.get("CreationDate", ""),
                "modified": meta.get("ModDate", ""),
            }
```

---

### 4.5. `tools/parsers/analyzers/keyword_matcher.py`

```python
"""
Tier 1: Python Keyword Matching
Fast, local analysis using keyword matching against scope definitions
"""

from typing import List, Dict, Optional
from collections import defaultdict

from ..config.div07_scopes import DIV07_SCOPES, get_scope
from ..config.drawing_types import classify_drawing, get_relevance, get_critical_types
from ..models.schemas import (
    PageExtraction, PageClassification, ScopeMatch, ScopeAnalysis,
    DrawingType, Relevance, AnalysisTier
)


class KeywordMatcher:
    """
    Tier 1 analyzer using Python keyword matching.
    ~95% of analysis should be handled here.
    """
    
    def __init__(self, scopes: Optional[List[str]] = None):
        """
        Initialize with specific scopes or all scopes.
        
        Args:
            scopes: List of scope IDs (e.g., ["071000", "072000"]) or None for all
        """
        if scopes:
            self.scopes = {sid: DIV07_SCOPES[sid] for sid in scopes if sid in DIV07_SCOPES}
        else:
            self.scopes = DIV07_SCOPES
    
    def classify_page(self, extraction: PageExtraction) -> PageClassification:
        """Classify a page by drawing type."""
        text = extraction.raw_text
        sheet = extraction.sheet_number or ""
        
        drawing_type_str = classify_drawing(text, sheet)
        
        # Map string to enum
        try:
            drawing_type = DrawingType(drawing_type_str)
        except ValueError:
            drawing_type = DrawingType.OTHER
        
        relevance_str = get_relevance(drawing_type_str)
        try:
            relevance = Relevance(relevance_str)
        except ValueError:
            relevance = Relevance.LOW
        
        # Calculate confidence based on match quality
        confidence = 0.8 if drawing_type != DrawingType.OTHER else 0.3
        
        return PageClassification(
            page_number=extraction.page_number,
            sheet_number=extraction.sheet_number,
            drawing_type=drawing_type,
            relevance=relevance,
            confidence=confidence,
            classified_by=AnalysisTier.PYTHON,
        )
    
    def match_scope(self, 
                    extraction: PageExtraction,
                    classification: PageClassification,
                    scope_id: str) -> Optional[ScopeMatch]:
        """
        Match a page against a specific scope.
        Returns ScopeMatch if relevant, None otherwise.
        """
        scope = self.scopes.get(scope_id)
        if not scope:
            return None
        
        text_lower = extraction.raw_text.lower()
        keywords = scope.get("keywords", [])
        
        # Find matching keywords
        matched = []
        for kw in keywords:
            if kw.lower() in text_lower:
                matched.append(kw)
        
        if not matched:
            return None
        
        # Calculate relevance score
        # More matches = higher score, critical drawing types = bonus
        base_score = min(len(matched) / 5.0, 1.0)  # Cap at 5 matches
        
        if classification.relevance == Relevance.CRITICAL:
            relevance_score = min(base_score + 0.3, 1.0)
        elif classification.relevance == Relevance.HIGH:
            relevance_score = min(base_score + 0.15, 1.0)
        else:
            relevance_score = base_score
        
        return ScopeMatch(
            scope_id=scope_id,
            scope_name=scope["name"],
            page_number=extraction.page_number,
            sheet_number=extraction.sheet_number,
            drawing_type=classification.drawing_type,
            matched_keywords=matched[:10],  # Top 10
            relevance_score=relevance_score,
            notes=None,
        )
    
    def analyze_scope(self, 
                      extractions: List[PageExtraction],
                      classifications: List[PageClassification],
                      scope_id: str) -> ScopeAnalysis:
        """
        Complete Tier 1 analysis for a scope.
        """
        scope = self.scopes.get(scope_id, {})
        
        matched_pages = []
        sheets_by_type = defaultdict(int)
        
        for extraction, classification in zip(extractions, classifications):
            match = self.match_scope(extraction, classification, scope_id)
            if match:
                matched_pages.append(match)
                sheets_by_type[classification.drawing_type.value] += 1
        
        # Identify critical sheets
        critical_types = get_critical_types()
        critical_sheets = [
            m for m in matched_pages 
            if m.drawing_type.value in critical_types
        ]
        
        # Estimate shop drawings needed
        shop_drawing_estimate = self._estimate_shop_drawings(
            matched_pages, sheets_by_type, scope_id
        )
        
        return ScopeAnalysis(
            scope_id=scope_id,
            scope_name=scope.get("name", scope_id),
            short_code=scope.get("short", scope_id[:3]),
            total_sheets=len(matched_pages),
            sheets_by_type=dict(sheets_by_type),
            matched_pages=matched_pages,
            critical_sheets=critical_sheets,
            shop_drawing_estimate=shop_drawing_estimate,
            analysis_tier=AnalysisTier.PYTHON,
            analysis_notes=None,
        )
    
    def _estimate_shop_drawings(self,
                                 matched_pages: List[ScopeMatch],
                                 sheets_by_type: Dict[str, int],
                                 scope_id: str) -> Dict:
        """Estimate shop drawing requirements based on matches."""
        scope = self.scopes.get(scope_id, {})
        requirements = scope.get("shop_drawing_requirements", {})
        
        # Count by category
        plans = sheets_by_type.get("Floor Plan", 0) + \
                sheets_by_type.get("Roof Plan", 0) + \
                sheets_by_type.get("Site Plan", 0)
        
        elevations = sheets_by_type.get("Exterior Elevation", 0)
        
        sections = sheets_by_type.get("Wall Section", 0) + \
                   sheets_by_type.get("Building Section", 0)
        
        details = sheets_by_type.get("Detail", 0)
        
        structural = sheets_by_type.get("Structural Foundation", 0) + \
                     sheets_by_type.get("Structural Framing", 0)
        
        # Rough estimate: each reference sheet may need 0.5-2 shop drawing details
        estimated_details = int(details * 1.5 + sections * 2 + plans * 0.5)
        
        return {
            "reference_sheets": {
                "plans": plans,
                "elevations": elevations,
                "sections": sections,
                "details": details,
                "structural": structural,
                "total": len(matched_pages),
            },
            "estimated_shop_drawings": {
                "plan_sheets": max(1, plans // 2),
                "detail_sheets": max(1, estimated_details // 10),
                "total_estimate": max(2, (plans // 2) + (estimated_details // 10) + (sections // 3)),
            },
            "requirements_from_spec": requirements,
        }
    
    def analyze_all_scopes(self,
                           extractions: List[PageExtraction],
                           classifications: List[PageClassification]) -> Dict[str, ScopeAnalysis]:
        """Analyze all selected scopes."""
        results = {}
        
        for scope_id in self.scopes:
            results[scope_id] = self.analyze_scope(
                extractions, classifications, scope_id
            )
        
        return results
```

---

### 4.6. `tools/parsers/analyzers/groq_analyzer.py`

```python
"""
Tier 2: Groq Llama 3.3 70B Analysis
For deeper analysis when Tier 1 keyword matching needs enhancement
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
import time

from groq import Groq

from ..config.div07_scopes import get_scope
from ..models.schemas import (
    PageExtraction, ScopeMatch, GroqAnalysis, AnalysisTier
)


class GroqAnalyzer:
    """
    Tier 2 analyzer using Groq Llama 3.3 70B.
    ~4% of analysis - when keyword matching is insufficient.
    
    Response time: ~395ms typical
    """
    
    MODEL = "llama-3.3-70b-versatile"
    
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment")
        
        self.client = Groq(api_key=api_key)
    
    def _build_system_prompt(self, scope_id: str) -> str:
        """Build system prompt for scope analysis."""
        scope = get_scope(scope_id)
        
        return f"""You are a construction document analyst specializing in Division 07 - Thermal and Moisture Protection.

You are analyzing drawings for: {scope.get('name', scope_id)}
Scope ID: {scope_id}

Your task is to identify:
1. Specific items shown in the drawing relevant to this scope
2. Conditions that require shop drawing details
3. Coordination items with other trades
4. Recommendations for shop drawing creation

Be specific and technical. Reference actual construction details and conditions.
Respond in JSON format only."""

    def _build_analysis_prompt(self, 
                                page_text: str,
                                sheet_number: str,
                                drawing_type: str,
                                matched_keywords: List[str]) -> str:
        """Build analysis prompt for a page."""
        return f"""Analyze this construction drawing page for shop drawing requirements.

Sheet: {sheet_number or 'Unknown'}
Drawing Type: {drawing_type}
Keywords Found: {', '.join(matched_keywords)}

Page Content:
{page_text[:3000]}

Respond with JSON:
{{
    "identified_items": ["list of specific items shown relevant to this scope"],
    "conditions": ["list of conditions requiring detail (e.g., 'foundation wall at grade transition')"],
    "coordination_items": ["items requiring coordination with other trades"],
    "recommendations": ["specific recommendations for shop drawing details"],
    "confidence": 0.0-1.0
}}"""

    def analyze_page(self,
                     extraction: PageExtraction,
                     scope_match: ScopeMatch) -> GroqAnalysis:
        """
        Analyze a single page with Groq.
        """
        start_time = time.time()
        
        system_prompt = self._build_system_prompt(scope_match.scope_id)
        user_prompt = self._build_analysis_prompt(
            extraction.raw_text,
            extraction.sheet_number or "",
            scope_match.drawing_type.value,
            scope_match.matched_keywords,
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
                response_format={"type": "json_object"},
            )
            
            result_text = response.choices[0].message.content
            result = json.loads(result_text)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return GroqAnalysis(
                scope_id=scope_match.scope_id,
                page_number=extraction.page_number,
                sheet_number=extraction.sheet_number,
                analysis_text=result_text,
                identified_items=result.get("identified_items", []),
                conditions=result.get("conditions", []),
                recommendations=result.get("recommendations", []),
                confidence=result.get("confidence", 0.7),
                processing_time_ms=processing_time,
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            
            return GroqAnalysis(
                scope_id=scope_match.scope_id,
                page_number=extraction.page_number,
                sheet_number=extraction.sheet_number,
                analysis_text=f"Error: {str(e)}",
                identified_items=[],
                conditions=[],
                recommendations=[],
                confidence=0.0,
                processing_time_ms=processing_time,
            )
    
    def analyze_batch(self,
                      extractions: List[PageExtraction],
                      scope_matches: List[ScopeMatch],
                      max_pages: int = 10) -> List[GroqAnalysis]:
        """
        Analyze a batch of pages.
        Limit to critical/high relevance pages.
        """
        results = []
        
        # Sort by relevance score, take top N
        sorted_matches = sorted(
            zip(extractions, scope_matches),
            key=lambda x: x[1].relevance_score,
            reverse=True
        )[:max_pages]
        
        for extraction, match in sorted_matches:
            analysis = self.analyze_page(extraction, match)
            results.append(analysis)
        
        return results
    
    def should_escalate_to_claude(self, groq_analyses: List[GroqAnalysis]) -> bool:
        """
        Determine if Claude analysis is needed.
        Escalate if:
        - Low confidence results
        - Complex conditions identified
        - Coordination issues found
        """
        if not groq_analyses:
            return False
        
        avg_confidence = sum(a.confidence for a in groq_analyses) / len(groq_analyses)
        
        # Low average confidence
        if avg_confidence < 0.6:
            return True
        
        # Many coordination items (complex project)
        total_coordination = sum(len(a.conditions) for a in groq_analyses)
        if total_coordination > 20:
            return True
        
        return False
```

---

### 4.7. `tools/parsers/analyzers/claude_analyzer.py`

```python
"""
Tier 3: Anthropic Claude Deep Analysis
For complex cases requiring comprehensive understanding
~1% of analysis - final escalation tier
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
import time

import anthropic

from ..config.div07_scopes import get_scope
from ..models.schemas import (
    PageExtraction, ScopeMatch, GroqAnalysis, ClaudeAnalysis
)


class ClaudeAnalyzer:
    """
    Tier 3 analyzer using Anthropic Claude.
    ~1% of analysis - complex cases only.
    
    Used for:
    - Comprehensive multi-page analysis
    - Complex coordination requirements
    - Shop drawing scope estimation
    - Quality assurance on Tier 2 results
    """
    
    MODEL = "claude-sonnet-4-20250514"
    
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set in environment")
        
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def _build_system_prompt(self, scope_id: str) -> str:
        """Build comprehensive system prompt."""
        scope = get_scope(scope_id)
        
        requirements = scope.get("shop_drawing_requirements", {})
        manufacturers = scope.get("manufacturers", [])
        
        return f"""You are a senior construction document analyst and shop drawing coordinator at Lefebvre Design Solutions, specializing in Division 07 - Thermal and Moisture Protection.

CURRENT SCOPE: {scope.get('name', scope_id)} ({scope_id})
DESCRIPTION: {scope.get('description', '')}

SHOP DRAWING REQUIREMENTS FOR THIS SCOPE:
{json.dumps(requirements, indent=2)}

COMMON MANUFACTURERS: {', '.join(manufacturers[:5])}

YOUR EXPERTISE:
- 20+ years experience in roofing and waterproofing
- Deep knowledge of construction details and assemblies
- Understanding of spec sections and submittal requirements
- Ability to identify coordination issues between trades

YOUR TASK:
Provide comprehensive analysis for shop drawing creation. Be specific about:
1. Every detail type needed with count estimates
2. Special conditions requiring unique details
3. Coordination items with other Division 07 sections
4. Coordination with structural, mechanical, electrical
5. Specific shop drawing sheet recommendations

Respond in structured JSON format."""

    def _build_comprehensive_prompt(self,
                                     extractions: List[PageExtraction],
                                     scope_matches: List[ScopeMatch],
                                     groq_analyses: Optional[List[GroqAnalysis]] = None) -> str:
        """Build prompt for comprehensive analysis."""
        
        # Compile page summaries
        page_summaries = []
        for ext, match in zip(extractions, scope_matches):
            summary = f"""
Page {ext.page_number} | Sheet: {ext.sheet_number or 'N/A'} | Type: {match.drawing_type.value}
Keywords: {', '.join(match.matched_keywords[:5])}
Preview: {ext.text_preview[:300]}"""
            page_summaries.append(summary)
        
        # Include Groq findings if available
        groq_summary = ""
        if groq_analyses:
            conditions = []
            items = []
            for ga in groq_analyses:
                conditions.extend(ga.conditions)
                items.extend(ga.identified_items)
            
            groq_summary = f"""
TIER 2 (GROQ) FINDINGS:
Identified Items: {', '.join(set(items)[:20])}
Conditions Found: {', '.join(set(conditions)[:15])}"""
        
        return f"""Analyze these construction drawing pages for comprehensive shop drawing requirements.

PAGES TO ANALYZE:
{''.join(page_summaries[:30])}

{groq_summary}

Provide comprehensive analysis in JSON format:
{{
    "detail_inventory": {{
        "foundation_details": <count>,
        "wall_section_details": <count>,
        "penetration_details": <count>,
        "transition_details": <count>,
        "flashing_details": <count>,
        "termination_details": <count>,
        "corner_details": <count>,
        "other_details": <count>
    }},
    "special_conditions": ["list of unique conditions requiring special details"],
    "coordination_items": ["list of items requiring coordination with other trades/specs"],
    "shop_drawing_recommendations": [
        "Specific recommendation 1 with sheet suggestion",
        "Specific recommendation 2 with detail count"
    ],
    "estimated_shop_drawing_sheets": <total count>,
    "priority_sheets": ["list of most important reference sheets to review first"],
    "notes": "Any additional observations for shop drawing creation"
}}"""

    def analyze_scope(self,
                      extractions: List[PageExtraction],
                      scope_matches: List[ScopeMatch],
                      scope_id: str,
                      groq_analyses: Optional[List[GroqAnalysis]] = None) -> ClaudeAnalysis:
        """
        Comprehensive Claude analysis for a scope.
        """
        start_time = time.time()
        
        # Filter to matched pages only
        matched_extractions = []
        matched_scope_matches = []
        for ext in extractions:
            for match in scope_matches:
                if ext.page_number == match.page_number:
                    matched_extractions.append(ext)
                    matched_scope_matches.append(match)
                    break
        
        system_prompt = self._build_system_prompt(scope_id)
        user_prompt = self._build_comprehensive_prompt(
            matched_extractions,
            matched_scope_matches,
            groq_analyses
        )
        
        try:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
            )
            
            result_text = response.content[0].text
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{[\s\S]*\}', result_text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {"error": "Could not parse JSON response"}
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return ClaudeAnalysis(
                scope_id=scope_id,
                page_numbers=[m.page_number for m in matched_scope_matches],
                comprehensive_analysis=result_text,
                detail_inventory=result.get("detail_inventory", {}),
                special_conditions=result.get("special_conditions", []),
                coordination_items=result.get("coordination_items", []),
                shop_drawing_recommendations=result.get("shop_drawing_recommendations", []),
                estimated_shop_drawing_count=result.get("estimated_shop_drawing_sheets", 0),
                processing_time_ms=processing_time,
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            
            return ClaudeAnalysis(
                scope_id=scope_id,
                page_numbers=[m.page_number for m in matched_scope_matches],
                comprehensive_analysis=f"Error: {str(e)}",
                detail_inventory={},
                special_conditions=[],
                coordination_items=[],
                shop_drawing_recommendations=[],
                estimated_shop_drawing_count=0,
                processing_time_ms=processing_time,
            )
    
    def quality_check(self,
                      scope_analysis: 'ScopeAnalysis',
                      groq_analyses: List[GroqAnalysis]) -> Dict:
        """
        QA check on Tier 1 and Tier 2 results.
        Returns validation and corrections.
        """
        # Build summary of findings
        summary = f"""
TIER 1 FINDINGS:
- Total sheets: {scope_analysis.total_sheets}
- By type: {json.dumps(scope_analysis.sheets_by_type)}
- Critical sheets: {len(scope_analysis.critical_sheets)}

TIER 2 FINDINGS:
- Pages analyzed: {len(groq_analyses)}
- Avg confidence: {sum(a.confidence for a in groq_analyses) / len(groq_analyses) if groq_analyses else 0:.2f}
- Total conditions: {sum(len(a.conditions) for a in groq_analyses)}
"""
        
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""Review this analysis for {scope_analysis.scope_name}:

{summary}

Provide brief QA assessment:
1. Is the sheet count reasonable?
2. Are critical drawing types identified?
3. Any obvious gaps in analysis?

Respond concisely."""
                }
            ],
        )
        
        return {
            "qa_assessment": response.content[0].text,
            "validated": True,
        }
```

---

### 4.8. `tools/parsers/main.py`

```python
"""
Division 07 Drawing Parser - CLI Entry Point
Lefebvre Design Solutions
"""

import argparse
import sys
import os
import json
from datetime import datetime
from typing import List, Optional

from .config.div07_scopes import DIV07_SCOPES
from .extractors.pdf_extractor import PDFExtractor
from .analyzers.keyword_matcher import KeywordMatcher
from .analyzers.groq_analyzer import GroqAnalyzer
from .analyzers.claude_analyzer import ClaudeAnalyzer
from .models.schemas import ParseResult, ParserConfig, AnalysisTier
from .outputs.report_generator import ReportGenerator
from .outputs.csv_exporter import CSVExporter
from .outputs.json_exporter import JSONExporter


def print_scope_menu():
    """Print interactive scope selection menu."""
    print("\n" + "=" * 60)
    print("DIVISION 07 SCOPES")
    print("=" * 60)
    
    for i, (scope_id, scope) in enumerate(DIV07_SCOPES.items(), 1):
        print(f"  {i:2}. [{scope['short']:5}] {scope_id} - {scope['name']}")
    
    print(f"\n   A. ALL SCOPES")
    print(f"   Q. QUIT")
    print("=" * 60)


def select_scopes_interactive() -> List[str]:
    """Interactive scope selection."""
    print_scope_menu()
    
    print("\nEnter numbers separated by commas (e.g., 1,2) or 'A' for all:")
    
    try:
        choice = input("> ").strip().upper()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        sys.exit(0)
    
    scope_list = list(DIV07_SCOPES.keys())
    
    if choice == "Q":
        sys.exit(0)
    elif choice == "A":
        return scope_list
    else:
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(",")]
            return [scope_list[i] for i in indices if 0 <= i < len(scope_list)]
        except (ValueError, IndexError):
            print("Invalid selection. Using all scopes.")
            return scope_list


def progress_callback(current: int, total: int):
    """Print progress dots."""
    if current % 10 == 0 or current == total:
        print(f"  Extracted {current}/{total} pages", end="\r")


def run_parser(config: ParserConfig) -> ParseResult:
    """
    Execute the full parsing pipeline.
    
    Tier 1: Python/pdfplumber extraction + keyword matching
    Tier 2: Groq Llama analysis (if enabled)
    Tier 3: Anthropic Claude analysis (if enabled and escalated)
    """
    start_time = datetime.utcnow()
    
    print("\n" + "=" * 60)
    print("DIVISION 07 DRAWING PARSER")
    print("Lefebvre Design Solutions")
    print("=" * 60)
    
    # =========================================================================
    # TIER 1: Python Extraction
    # =========================================================================
    print(f"\n[TIER 1] Extracting PDF: {os.path.basename(config.pdf_path)}")
    
    extractor = PDFExtractor(config.pdf_path)
    metadata = extractor.get_metadata()
    print(f"  File: {metadata['file_name']}")
    print(f"  Pages: {metadata['total_pages']}")
    print(f"  Size: {metadata['file_size_bytes'] / (1024*1024):.1f} MB")
    
    extractions = extractor.extract_all_list(progress_callback)
    print(f"\n  ✓ Extracted {len(extractions)} pages")
    
    # =========================================================================
    # TIER 1: Classification + Keyword Matching
    # =========================================================================
    print(f"\n[TIER 1] Analyzing for scopes: {', '.join(config.selected_scopes)}")
    
    matcher = KeywordMatcher(config.selected_scopes)
    
    # Classify all pages
    classifications = [matcher.classify_page(ext) for ext in extractions]
    print(f"  ✓ Classified {len(classifications)} pages")
    
    # Analyze each scope
    scope_analyses = matcher.analyze_all_scopes(extractions, classifications)
    
    total_relevant = sum(sa.total_sheets for sa in scope_analyses.values())
    print(f"  ✓ Found {total_relevant} relevant sheets across {len(scope_analyses)} scopes")
    
    # Initialize result
    result = ParseResult(
        document_name=metadata['file_name'],
        document_path=config.pdf_path,
        total_pages=len(extractions),
        selected_scopes=config.selected_scopes,
        extractions=extractions,
        classifications=classifications,
        scope_analyses=scope_analyses,
        total_relevant_sheets=total_relevant,
    )
    
    # =========================================================================
    # TIER 2: Groq Analysis (Optional)
    # =========================================================================
    if config.enable_groq and total_relevant > 0:
        print(f"\n[TIER 2] Groq Llama 3.3 70B Analysis")
        
        try:
            groq = GroqAnalyzer()
            groq_analyses = []
            
            for scope_id, scope_analysis in scope_analyses.items():
                if scope_analysis.total_sheets == 0:
                    continue
                
                print(f"  Analyzing {scope_analysis.short_code}...", end=" ")
                
                # Get extractions for matched pages
                matched_extractions = [
                    ext for ext in extractions
                    if any(m.page_number == ext.page_number for m in scope_analysis.matched_pages)
                ]
                
                batch_analyses = groq.analyze_batch(
                    matched_extractions,
                    scope_analysis.matched_pages,
                    max_pages=config.groq_batch_size
                )
                
                groq_analyses.extend(batch_analyses)
                print(f"✓ ({len(batch_analyses)} pages)")
            
            result.groq_analyses = groq_analyses
            print(f"  ✓ Tier 2 complete: {len(groq_analyses)} pages analyzed")
            
            # Check if Claude escalation needed
            escalate = groq.should_escalate_to_claude(groq_analyses)
            
        except Exception as e:
            print(f"  ⚠ Groq analysis failed: {e}")
            escalate = config.enable_claude  # Escalate anyway if Claude enabled
    else:
        escalate = config.enable_claude and total_relevant > 0
    
    # =========================================================================
    # TIER 3: Claude Analysis (Optional, Escalated)
    # =========================================================================
    if config.enable_claude and escalate and total_relevant > 0:
        print(f"\n[TIER 3] Anthropic Claude Deep Analysis")
        
        try:
            claude = ClaudeAnalyzer()
            claude_analyses = []
            
            for scope_id, scope_analysis in scope_analyses.items():
                if scope_analysis.total_sheets == 0:
                    continue
                
                print(f"  Deep analysis: {scope_analysis.short_code}...", end=" ")
                
                # Get Groq analyses for this scope
                scope_groq = [
                    ga for ga in (result.groq_analyses or [])
                    if ga.scope_id == scope_id
                ]
                
                claude_result = claude.analyze_scope(
                    extractions,
                    scope_analysis.matched_pages,
                    scope_id,
                    scope_groq
                )
                
                claude_analyses.append(claude_result)
                print(f"✓ ({claude_result.estimated_shop_drawing_count} sheets est.)")
            
            result.claude_analyses = claude_analyses
            print(f"  ✓ Tier 3 complete: {len(claude_analyses)} scopes analyzed")
            
        except Exception as e:
            print(f"  ⚠ Claude analysis failed: {e}")
    
    # Calculate processing time
    end_time = datetime.utcnow()
    result.processing_time_ms = int((end_time - start_time).total_seconds() * 1000)
    
    return result


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Division 07 Drawing Parser - Lefebvre Design Solutions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m tools.parsers.main drawings.pdf
  python -m tools.parsers.main drawings.pdf --scope 071000,072000
  python -m tools.parsers.main drawings.pdf --all --no-claude
        """
    )
    
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("--scope", "-s", help="Comma-separated scope IDs (e.g., 071000,072000)")
    parser.add_argument("--all", "-a", action="store_true", help="Analyze all scopes")
    parser.add_argument("--no-groq", action="store_true", help="Disable Groq analysis")
    parser.add_argument("--no-claude", action="store_true", help="Disable Claude analysis")
    parser.add_argument("--output", "-o", default="./output", help="Output directory")
    parser.add_argument("--format", "-f", default="txt,csv,json", help="Output formats (txt,csv,json)")
    
    args = parser.parse_args()
    
    # Validate PDF
    if not os.path.exists(args.pdf):
        print(f"ERROR: File not found: {args.pdf}")
        sys.exit(1)
    
    # Select scopes
    if args.all:
        selected_scopes = list(DIV07_SCOPES.keys())
    elif args.scope:
        selected_scopes = [s.strip() for s in args.scope.split(",")]
        # Validate
        invalid = [s for s in selected_scopes if s not in DIV07_SCOPES]
        if invalid:
            print(f"ERROR: Invalid scope IDs: {invalid}")
            print(f"Valid scopes: {list(DIV07_SCOPES.keys())}")
            sys.exit(1)
    else:
        selected_scopes = select_scopes_interactive()
    
    if not selected_scopes:
        print("No scopes selected. Exiting.")
        sys.exit(1)
    
    # Build config
    config = ParserConfig(
        pdf_path=args.pdf,
        selected_scopes=selected_scopes,
        enable_groq=not args.no_groq,
        enable_claude=not args.no_claude,
        output_dir=args.output,
        output_formats=[f.strip() for f in args.format.split(",")],
    )
    
    # Run parser
    result = run_parser(config)
    
    # Generate outputs
    print(f"\n[OUTPUT] Generating reports...")
    
    os.makedirs(config.output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(config.pdf_path))[0]
    
    if "txt" in config.output_formats:
        report_gen = ReportGenerator()
        report_path = os.path.join(config.output_dir, f"{base_name}_REPORT.txt")
        report_gen.generate(result, report_path)
        print(f"  ✓ Report: {report_path}")
    
    if "csv" in config.output_formats:
        csv_exp = CSVExporter()
        csv_path = os.path.join(config.output_dir, f"{base_name}_DATA.csv")
        csv_exp.export(result, csv_path)
        print(f"  ✓ CSV: {csv_path}")
    
    if "json" in config.output_formats:
        json_exp = JSONExporter()
        json_path = os.path.join(config.output_dir, f"{base_name}_DATA.json")
        json_exp.export(result, json_path)
        print(f"  ✓ JSON: {json_path}")
    
    # Print summary
    print(f"\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Pages: {result.total_pages}")
    print(f"Relevant Sheets: {result.total_relevant_sheets}")
    print(f"Processing Time: {result.processing_time_ms}ms")
    print(f"\nBy Scope:")
    for scope_id, analysis in result.scope_analyses.items():
        print(f"  {analysis.short_code}: {analysis.total_sheets} sheets")
        if result.claude_analyses:
            claude = next((c for c in result.claude_analyses if c.scope_id == scope_id), None)
            if claude:
                print(f"       → Est. Shop Drawings: {claude.estimated_shop_drawing_count}")
    
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
```

---

## 5. REMAINING FILES TO CREATE

The following files need to be created with proper implementations:

### Still Required:
- `tools/parsers/__init__.py` - Package init
- `tools/parsers/config/__init__.py`
- `tools/parsers/extractors/__init__.py`
- `tools/parsers/extractors/text_processor.py`
- `tools/parsers/analyzers/__init__.py`
- `tools/parsers/models/__init__.py`
- `tools/parsers/outputs/__init__.py`
- `tools/parsers/outputs/report_generator.py`
- `tools/parsers/outputs/csv_exporter.py`
- `tools/parsers/outputs/json_exporter.py`
- `tools/parsers/api.py` - FastAPI router
- `roofio-backend/api/routes/parser.py` - Backend integration
- `tests/parsers/*` - All test files
- `docs/PARSER.md` - Documentation

---

## 6. VALIDATION COMMANDS

Before committing, run:

```bash
# Install dependencies
pip install pdfplumber groq anthropic pydantic pytest

# Test imports
python -c "from tools.parsers.main import run_parser; print('OK')"

# Run tests
cd tests && python -m pytest parsers/ -v

# Test with sample PDF
python -m tools.parsers.main sample.pdf --scope 071000 --no-groq --no-claude
```

---

## 7. ENVIRONMENT VARIABLES REQUIRED

Add to `.env`:

```bash
# Tier 2: Groq
GROQ_API_KEY=gsk_...

# Tier 3: Anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

**CRITICAL:** Do NOT use hardcoded defaults. Fail fast if not set.

---

## 8. INTEGRATION WITH EXISTING SYSTEM

### Database Table (add to `unified_schema.sql`):

```sql
-- Parse results storage
CREATE TABLE IF NOT EXISTS parse_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agency_id UUID NOT NULL REFERENCES agencies(agency_id),
    project_id UUID REFERENCES projects(project_id),
    document_name VARCHAR(255) NOT NULL,
    document_hash VARCHAR(64) NOT NULL,
    selected_scopes TEXT[] NOT NULL,
    total_pages INTEGER NOT NULL,
    total_relevant_sheets INTEGER NOT NULL,
    result_data JSONB NOT NULL,
    processing_time_ms INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(user_id),
    
    UNIQUE(agency_id, document_hash)
);

CREATE INDEX idx_parse_results_agency ON parse_results(agency_id);
CREATE INDEX idx_parse_results_project ON parse_results(project_id);
```

---

## 9. SESSION LOG ENTRY

After completing this work, add to `SESSION-LOG.md`:

```markdown
## Session: Division 07 Parser Integration

**Date:** [DATE]
**Duration:** [TIME]

### What Was Done
- Created modular Division 07 drawing parser
- Implemented 3-tier AI analysis: Python → Groq → Claude
- Added all 9 Division 07 scopes with keywords
- Created CLI and API interfaces
- Integrated with multi-tenant database

### Problems Encountered
- [List any issues]

### Solutions Applied
- [List solutions]

### Next Steps
- [ ] Add remaining output generators
- [ ] Complete test coverage
- [ ] Deploy to staging
```

---

## 10. CRITICAL REMINDERS

1. **NO QUICK FIXES** - Follow the architecture
2. **Atomic commits** - One logical unit per commit
3. **Test first** - Run validation before committing
4. **agency_id** - Always include for multi-tenancy
5. **Fail fast** - Validate environment variables
6. **Document** - Update CLAUDE.md if architecture changes

---

*Instructions prepared for Claude Code*
*Lefebvre Design Solutions*
*December 2025*
