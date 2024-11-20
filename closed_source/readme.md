# Gemini AI Tender Document Extraction Tool

## Overview
This Python script uses Google's Gemini AI to automatically extract structured information from tender documents. It's designed to parse PDF tender documents and extract key details such as basic information, timeline, financial requirements, technical specifications, and more.

## Prerequisites
- Python 3.8+
- Google Generative AI API access
- A valid Gemini API key

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://your-repository-url.git
cd tender-extraction-tool
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root and add your Gemini API key:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Script Functionality

### Key Features
- Uploads PDF tender documents to Gemini
- Extracts structured JSON data from the document
- Handles file processing and waiting
- Configurable generation settings

### Extraction Details
The script extracts the following key information:
- Basic Tender Information
- Timeline and Important Dates
- Financial Requirements
- Eligibility Criteria
- Technical Specifications
- Contact Information
- Legal and Compliance Details

### Configuration Parameters
- `temperature`: Controls randomness in generation (1.0 = most random)
- `top_p`: Nucleus sampling threshold
- `top_k`: Top-k tokens consideration
- `max_output_tokens`: Maximum response length

## Usage

### Running the Script
```bash
python Gemini.py
```

### Customization
- Modify `generation_config` to adjust AI generation parameters
- Update `system_instruction` to refine extraction criteria

## Error Handling
- Checks file processing status
- Raises exceptions for unprocessed files
- Validates file upload and processing

## Dependencies
- `google-generativeai`: Google's Generative AI library
- `python-dotenv`: Manages environment variables
- `os`: System interaction
- `time`: Delay and waiting mechanisms

## Limitations
- Requires a valid Gemini API key
- Performance depends on document clarity and structure
- Best suited for structured tender documents
