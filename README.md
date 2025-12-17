# Assembly Drawing Archive Tool

A Flask-based web application for parsing and extracting structured data from roofing shop drawings, including scope of work documents, specifications, architectural drawings, and assembly letters.

## Features

- **Multi-Document Parsing**: Upload and parse multiple document types simultaneously
- **Large Drawing Set Parser**: Process 1500+ page architectural drawing sets to find roofing details
  - Two-stage filtering: Python filters ~95% of irrelevant pages
  - AI Vision Analysis: Claude vision analyzes filtered pages for detailed extraction
- **Assembly Letter Extraction**: Comprehensive parsing of roof assembly details including:
  - Multiple assembly detection (Main Roof, Receiving Room, Canopy, etc.)
  - Layer-by-layer breakdown (membranes, insulation, coverboards, vapor barriers)
  - Attachment methods and specifications
  - FM RoofNav, UL, and ASTM approvals
- **Scope of Work Parser**: Extracts materials, requirements, and project summaries
- **Specification Parser**: Identifies manufacturers and product specifications
- **Drawing Parser**: Extracts elements and callouts from architectural drawings
- **Drag & Drop Interface**: Modern, intuitive UI with file management
- **Multi-Manufacturer Support**: Works with Carlisle, Mule-Hide, GAF, Firestone, Johns Manville, Siplast, SOPREMA, Versico

## Installation

### Prerequisites
- Python 3.7+
- pip
- poppler-utils (for pdf2image - required for AI vision analysis)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/buildingsystemsai-drafty/AssemblyDrawingTool.git
   cd AssemblyDrawingTool
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **Mac/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. (Optional) Set up AI Vision Analysis:
   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

### Web Interface

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000`

3. Upload documents:
   - Drag and drop or click to upload PDFs in each category
   - Remove files by clicking the X button
   - Click "Parse Documents" to extract data

### Large Drawing Set Parser (API)

For processing large architectural drawing sets (like JFK Terminal 1 with 1500+ pages):

#### Filter Only (Stage 1 - Fast)
```bash
curl -X POST -F "drawing_set=@drawings.pdf" \
  "http://localhost:5000/filter-drawing-set?min_relevance=0.3"
```

#### Full Analysis with AI Vision (Stage 1 + Stage 2)
```bash
curl -X POST -F "drawing_set=@drawings.pdf" \
  "http://localhost:5000/parse-large-drawing-set?use_ai=true&min_relevance=0.3"
```

#### Command Line
```bash
# Basic usage
python parsers/large_drawing_set_parser.py drawings.pdf

# Test with first 100 pages
python parsers/large_drawing_set_parser.py drawings.pdf 100

# Start from specific page (e.g., page 641)
python parsers/large_drawing_set_parser.py drawings.pdf 20 --start 641

# Force AI analysis on all pages (bypasses filter)
python parsers/large_drawing_set_parser.py drawings.pdf 10 --start 641 --force-ai
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `<pdf_path>` | Path to the PDF file (required) |
| `<max_pages>` | Number of pages to analyze |
| `--start N` | Start from page N |
| `--force-ai` | Bypass filter and send all pages to AI |

### Installing Poppler (Required for AI Vision)

**Windows:**
1. Download from https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\poppler`
3. Add to PATH: `$env:Path += ";C:\poppler\Library\bin"`

**Mac:**
```bash
brew install poppler
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/parse` | POST | Parse scope, spec, drawing, assembly documents |
| `/parse-large-drawing-set` | POST | Parse large drawing sets with optional AI analysis |
| `/filter-drawing-set` | POST | Quick filter to identify roof-related sheets |

### Query Parameters for Large Drawing Set Endpoints

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `use_ai` | bool | false | Enable AI vision analysis |
| `max_pages` | int | all | Limit pages to analyze |
| `min_relevance` | float | 0.3 | Minimum relevance score (0.0-1.0) |

## Project Structure

```
AssemblyDrawingTool/
├── app.py                              # Main Flask application
├── requirements.txt                    # Python dependencies
├── README.md                           # Project documentation
├── CLAUDE.md                           # Claude Code guidance
├── parsers/
│   ├── __init__.py
│   ├── assembly_parser.py              # Assembly letter parser
│   ├── scope_parser.py                 # Scope of work parser
│   ├── spec_parser.py                  # Specification parser
│   ├── arch_drawing_parser.py          # Drawing parser (text-based)
│   ├── large_drawing_set_parser.py     # Large drawing set parser with AI vision
│   ├── pdf_extractor.py                # PDF text extraction
│   └── text_cleaner.py                 # Text cleaning utilities
├── generators/
│   └── dxf_generator.py                # DXF output generation
├── static/
│   └── js/
│       └── app.js                      # Frontend JavaScript
├── templates/
│   └── index.html                      # Main UI template
└── uploads/                            # Temporary file storage
```

## Large Drawing Set Parser

The `large_drawing_set_parser.py` is designed for massive architectural drawing sets (1500+ pages). It uses a two-stage approach:

### Stage 1: Python Filtering
- Analyzes sheet numbers (A5xx series = roof plans per AIA standards)
- Extracts text and searches for roofing keywords
- Scores each page for roof relevance
- Typically filters out 90-95% of non-roof pages

### Stage 2: AI Vision Analysis
- Converts filtered pages to images
- Sends to Claude Vision API for analysis
- Extracts:
  - Roof drains, scuppers, RTUs
  - Penetrations, skylights, hatches
  - Material specifications
  - Detail references
  - Square footage and scales

### Supported Sheet Number Patterns
- `A-5xx`, `A5xx`, `A5.xx` - Roof plans
- `A-8xx`, `A-9xx` - Architectural details
- `R-xx`, `RF-xx` - Roof-specific sheets

### Roofing Keywords Detected
- High relevance: roof plan, roof detail, membrane, TPO, EPDM, parapet, flashing
- Medium relevance: scupper, RTU, curb, penetration, tapered insulation
- Context: waterproof, drainage, slope, deck

## Technologies Used

- **Backend**: Flask (Python)
- **PDF Processing**: pdfplumber, PyPDF2, pdf2image
- **AI Vision**: Anthropic Claude API
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Custom CSS with gradient design

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API key for Claude vision analysis |
| `PORT` | Server port (default: 5000) |
| `FLASK_ENV` | Set to "production" to disable debug mode |

## Author

Armand Lefebvre - [roofshopdrawings.com](https://roofshopdrawings.com)

## License

This project is private and proprietary.
