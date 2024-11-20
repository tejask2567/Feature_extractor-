# Tender PDF Information Extraction Tool

## Overview
A sophisticated Python-based tool that leverages machine learning to extract structured information from tender PDF documents. Utilizes question-answering models and advanced text processing techniques to parse complex tender documents.

## Features
- PDF text extraction using `pdfplumber`
- Advanced text cleaning with NLTK
- Machine learning-powered information extraction
- Comprehensive logging
- JSON output generation

## Project Architecture
```
tender-extraction/
│
├── src/
│   └── BERT.py
├── inputs/
│   └── test.pdf
├── outputs/
│   └── output2.json
├── logs/
│   └── tender_extraction.log
├── requirements.txt
└── README.md
```

## Prerequisites
- Python 3.8+
- Minimum 8GB RAM
- GPU recommended for faster processing (optional)

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://your-repository-url.git
cd tender-extraction
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m nltk.downloader stopwords  # Download NLTK resources
```

## Configuration

### Customization Options
- Modify `questions` in `extract_with_qa()` to add or remove extraction fields
- Adjust logging levels in `logging.basicConfig()`
- Change QA model by updating `pipeline()` parameters

## Usage

### Running the Script
```bash
python BERT.py
```

### Command Line Arguments
Currently supports hardcoded PDF path. Future versions will include CLI arguments.

## Extraction Process

### Text Extraction Steps
1. Extract raw text from PDF using `pdfplumber`
2. Clean text by:
   - Removing stop words
   - Converting to lowercase
   - Removing extra whitespaces
3. Use DistilBERT QA model to extract specific information
4. Save results in JSON format

### Extracted Information
The script attempts to extract:
- Reference Number
- Tender Title
- Issuing Organization
- Contact Details
- Bid Timeline
- Financial Requirements
- Technical Specifications
- Eligibility Criteria
- Legal Jurisdiction
- And more...

## Logging
- Generates comprehensive logs at `tender_extraction.log`
- Tracks extraction process, errors, and performance metrics

## Error Handling
- Robust error management
- Graceful failure with detailed log messages
- Handles PDF reading, text extraction, and model inference errors

## Performance
- Extraction time depends on:
  - PDF complexity
  - Document length
  - System hardware

## Limitations
- Accuracy depends on document structure
- Works best with well-formatted PDFs
- Model performance varies with document complexity

## Dependencies
- `pdfplumber`: PDF text extraction
- `transformers`: Machine learning models
- `nltk`: Text preprocessing
- `torch`: Machine learning backend

## Troubleshooting
- Ensure NLTK resources are downloaded
- Check PDF formatting
- Verify model compatibility
- Review log files for detailed errors

## Future Improvements
- CLI argument support
- Multiple model support
- Enhanced error handling
- Performance optimization

