# Assembly Drawing Archive Tool

A Flask-based web application for parsing and extracting structured data from roofing shop drawings, including scope of work documents, specifications, architectural drawings, and assembly letters.

## Features

- **Multi-Document Parsing**: Upload and parse multiple document types simultaneously
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

### Setup

1. Extract the project files:
   ```bash
   unzip AssemblyDrawingTool-main.zip
   cd AssemblyDrawingTool-main
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

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000`

3. Upload documents:
   - Drag and drop or click to upload PDFs in each category
   - Remove files by clicking the X button
   - Click "Parse Documents" to extract data

4. View results: Parsed data is displayed in an organized format with project information, contractor details, assembly breakdowns, layer specifications, and approval ratings.

## Project Structure

```
AssemblyDrawingTool/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── parsers/
│   ├── __init__.py
│   ├── assembly_parser.py          # Assembly letter parser
│   ├── scope_parser.py             # Scope of work parser
│   ├── spec_parser.py              # Specification parser
│   ├── arch_drawing_parser.py      # Drawing parser
│   ├── pdf_extractor.py            # PDF text extraction
│   └── text_cleaner.py             # Text cleaning utilities
├── generators/
│   └── dxf_generator.py            # DXF output generation
├── static/
│   └── js/
│       └── app.js                  # Frontend JavaScript
├── templates/
│   └── index.html                  # Main UI template
└── uploads/                        # Temporary file storage
```

## Technologies Used

- **Backend**: Flask (Python)
- **PDF Processing**: PyPDF2
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Styling**: Custom CSS with gradient design
- **Text Processing**: Regex pattern matching

## Supported Document Types

### Assembly Letters
- Extracts up to 5 assemblies per document
- Parses 3 membrane layers, 3 insulation layers, 2 coverboards
- Captures attachment methods and specifications
- Identifies FM, UL, and ASTM approvals

### Scope of Work
- Materials and requirements
- Project summaries
- Budget items

### Specifications
- Manufacturer identification
- Product listings
- System specifications

### Drawings
- Element extraction
- Callout identification
- Drawing annotations

## Author

Armand Lefebvre - [roofshopdrawings.com](https://roofshopdrawings.com)

## License

This project is private and proprietary.
