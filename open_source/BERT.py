import pdfplumber
from transformers import pipeline
import logging
import time
import sys
import re
import json
import nltk
from nltk.corpus import stopwords

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('tender_extraction.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path):
  
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            logger.info(f"Processing PDF: {pdf_path}")
            logger.info(f"Total pages: {len(pdf.pages)}")
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                logger.debug(f"Extracted text from page {page_num}")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise

def clean_text(text):
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    

    stop_words = set(stopwords.words('english'))
    

    additional_stop_words = {
        'like', 'just', 'really', 'actually', 'would', 'could', 'should', 
        'might', 'may', 'now', 'going', 'get', 'got', 'yet', 'already'
    }

    all_stop_words = stop_words.union(additional_stop_words)
    

    text = re.sub(r"\n\s*\n", "\n", text)

    text = text.lower()

    words = text.split()

    filtered_words = [word for word in words if word not in all_stop_words]
    

    cleaned_text = ' '.join(filtered_words)
    

    return cleaned_text.strip()

def extract_with_qa(text, qa_model):
    questions = [
        ("reference_number", "What is the reference number in the tender?"),
        ("tender_title", "What is the title of the tender?"),
        ("issuing_organization", "What is the name of the issuing organization?"),
        ("contact_email", "What are the contact email addresses?"),
        ("contact_phone", "What are the contact phone numbers?"),
        ("start_date_for_bid_submissions", "What is the start date for bid submissions?"),
        ("online_bid_submission_deadline", "What is the deadline for online bid submission?"),
        ("physical_submission_deadline", "What is the deadline for physical submission of tender fee and EMD?"),
        ("technical_bid_opening_date", "What is the date for opening technical bids online?"),
        ("tender_fee", "What is the tender fee?"),
        ("Project_Scope", "What is the scope of work for the project outlined in the tender?"),
        ("emd", "What is the Earnest Money Deposit (EMD) amount required ?"),
        ("exemption_criteria", "What is the exemption criteria for tender fee and EMD?"),
        ("payment_terms", "What are the payment terms?"),
        ("Materials Required", "What materials or resources are required for the project as mentioned in the tender?"),
        ("Site_Location", "What is the location or site of the project?"),
        ("eligibility_criteria", "What are the eligibility criteria for bidders?"),
        ("technical_specifications", "What are the technical specifications for the equipment?"),
        ("delivery_time", "What is the delivery time mentioned in the tender?"),
        ("penalty_details", "What are the penalty details in case of delay?"),
        ("technical_evaluation_process", "What is the process for technical evaluation?"),
        ("financial_evaluation_process", "What is the process for financial evaluation?"),
        ("issuing_authority", "Who is the issuing authority of the tender?"),
        ("legal_jurisdiction", "What is the legal jurisdiction for disputes?"),
        ("arbitration_clause", "What is the arbitration clause for disputes?"),
    ]

    results = {}
    for field, question in questions:
        try:
            result = qa_model(question=question, context=text)
            results[field] = result["answer"]
            logger.info(f"Extracted {field}: {result['answer']}")
        except Exception as e:
            logger.warning(f"Could not extract {field}: {e}")
            results[field] = "Not found"
    return results

def save_output(data, output_file="output2.json"):

    try:
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)
        logger.info(f"Output saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving output: {e}")

def main(pdf_path):

    start_time = time.time()
    logger.info("Starting tender extraction process")

    try:

        logger.info("Loading QA model")
        qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

        text = extract_text_from_pdf(pdf_path)
        cleaned_text = clean_text(text)

        logger.info("Extracting tender information")
        extracted_data = extract_with_qa(cleaned_text, qa_model)
        
        save_output(extracted_data)

        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Extraction complete! Time taken: {execution_time:.2f} seconds")
        print(f"Extraction complete! Time taken: {execution_time:.2f} seconds. Results saved in 'output2.json'.")

    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        print(f"Extraction failed. Check 'tender_extraction.log' for details.")

if __name__ == "__main__":

    pdf_path = "test.pdf"
    main(pdf_path)
