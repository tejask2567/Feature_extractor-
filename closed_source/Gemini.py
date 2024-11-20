import os
import time
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):

  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
 
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  system_instruction="You are a model that extracts information from tender documents:\n\nBasic Information: Include the reference number, tender title, issuing organization, and contact email/phone numbers.\nTimeline Details: Extract key dates such as the start date for bid submissions, submission deadline, physical submission deadline, and technical bid opening date.\nFinancial Requirements: Identify tender fees (indicate if refundable or non-refundable), EMD amount, exemption criteria, and payment terms.\nEligibility Criteria: Extract details on required registrations, certifications, or specific eligibility conditions for participation.\nTechnical Specifications: Provide detailed specifications outlined for the equipment or service, particularly from sections labeled 'Annexure-A' or similar.\nContact Information: Extract the names, designations, email addresses, and phone numbers of key contacts.\nCompliance and Legal Details: Include any relevant compliance declarations, legal jurisdiction, arbitration clauses, and performance bond/guarantee details.\nOther Relevant Notes: Extract any additional important information or instructions that may affect the submission or evaluation process.\"",
)


files = [
  upload_to_gemini("document (1).pdf", mime_type="application/pdf"),
]

wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
        "Extract and structure the following details from the provided document in json\n",
      ],
    },
    {
      "role": "model",
      "parts": [
        "```json\n{\n  \"Basic Information\": {\n    \"Reference Number\": \"NITJ/DRC/PUR/TT/36/2024\",\n    \"Tender Title\": \"Fabrication of Machine for Continuous Production of Textile Waste Based Composite Materials\",\n    \"Issuing Organization\": \"Dr. B.R. Ambedkar National Institute of Technology, Jalandhar\",\n    \"Contact Email\": \"drc@nitj.ac.in\",\n    \"Contact Phone\": \"0181-2690301-453\"\n  },\n  \"Timeline Details\": {\n    \"Bid Submission Start Date\": \"16.10.2024 at 03:00 PM\",\n    \"Bid Submission Deadline\": \"06.11.2024 up to 03:00 PM\",\n    \"Physical Submission Deadline\": \"07.11.2024 up to 03:00 PM\",\n    \"Technical Bid Opening Date\": \"07.11.2024 at 03:00 PM\"\n  },\n  \"Financial Requirements\": {\n    \"Tender Fees\": \"Rs. 500/- (Non-refundable)\",\n    \"EMD Amount\": \"Rs. 90,000/-\",\n    \"EMD Exemption\": \"MSME/NSIC registered bidders\",\n    \"Payment Terms\": \"100% payment against physical delivery, inspection, installation, training, satisfactory working report, and receipt of Performance Bank Guarantee @ 3%\"\n  },\n  \"Eligibility Criteria\": {\n    \"Registrations\": \"MSME/NSIC registration for tender fee/EMD exemption\",\n    \"Other\": \"Class I and Class II Local Suppliers (as per Make in India guidelines). Non-Local Suppliers are not eligible.\"\n  },\n  \"Technical Specifications\": {\n    \"Details\": [\n      \"Capable of feeding textile materials in sheets and fibrous forms\",\n      \"Provision to coat textile materials with polymeric substances\",\n      \"Drying of coated textiles via heated calender rolls or suitable method\",\n      \"Cooling of coated textiles up to -10°C\",\n      \"Coating with thermoset and thermoplastic polymeric materials and curing\",\n      \"Modifications in process sequence as required\",\n      \"Cutting composite materials of desired sizes\",\n      \"Continuous production with desired length\",\n      \"Batching device for rolling prepregs/preforms\",\n      \"Fabrication in consultation with the indenter\",\n      \"Composite width of 4 feet\",\n      \"Indenter holds all intellectual property rights\",\n      \"Design may be changed during development\"\n    ],\n    \"Refer to\": \"Annexure-A\"\n  },\n  \"Contact Information\": {\n    \"Deputy Registrar (Research and Consultancy)\": {\n      \"Email\": \"gauravy@nitj.ac.in, drcpurchase@nitj.ac.in\"\n    },\n    \"Dean Research and Consultancy\": {\n      \"Name\": \"Dr. Rohit Mehra\",\n      \"Address\": \"Dr BR Ambedkar National Institute of Technology,\\nGT Road Amritsar By Pass, Jalandhar-144008, Punjab (India)\"\n    }\n  },\n  \"Compliance and Legal Details\": {\n    \"Declarations\": \"Declaration regarding blacklisting/debarring, Self Declaration for local content, Certificate of Land Border with India\",\n    \"Legal Jurisdiction\": \"Jalandhar Courts\",\n    \"Arbitration\": \"Sole Arbitrator appointed by the Institute, as per Arbitration and Conciliation Act, 1996\",\n    \"Performance Bond/Guarantee\": \"3% of total offer value, valid until warranty period + 2 months. Format in Annexure B & C.\"\n  },\n  \"Other Relevant Notes\": {\n    \"Only e-tenders accepted\",\n    \"No rates in technical bid\",\n    \"Director's decision is final\",\n    \"Offer valid for 120 days\",\n    \"Details about service centers in India should be mentioned.\"\n  }\n}\n```",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)