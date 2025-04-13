import argparse
import json
import logging
import os
import sys

import PyPDF2
import docx
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
GEMINI_MODEL_NAME = "gemini-2.0-flash"
# Lower safety settings for potentially less filtering, adjust if needed
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
GENERATION_CONFIG = {
    "temperature": 0.2,  # Lower temperature for more deterministic output
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 8192,  # Max for flash model
    "response_mime_type": "application/json",  # Request JSON output directly
}

# --- Fixed JSON Schema Definition ---
# This schema is embedded directly into the prompt
JSON_SCHEMA_DEFINITION = """
{
  "personal_information": {
    "name": "string | null",             // Full name
    "email": "string | null",            // Primary email address
    "phone": "string | null",            // Primary phone number
    "location": "string | null",         // City, State, Country etc.
    "linkedin_url": "string | null",     // URL to LinkedIn profile
    "portfolio_url": "string | null",    // URL to personal portfolio/website
    "github_url": "string | null",       // URL to GitHub profile
    "other_links": ["string"]            // List of other relevant URLs (e.g., blog, specific projects)
  },
  "summary": "string | null",            // Professional summary or objective statement
  "work_experience": [                   // List of work experiences, most recent first ideally
    {
      "job_title": "string | null",      // Job title/position
      "company": "string | null",        // Company name
      "location": "string | null",       // City, State of the job
      "start_date": "string | null",     // Start date (e.g., "Jan 2020", "2020-01")
      "end_date": "string | null",       // End date (e.g., "Dec 2022", "2022-12", "Present")
      "description": "string | null"     // Bullet points or paragraph describing responsibilities/achievements (combine bullets into one string if needed)
    }
  ],
  "education": [                         // List of educational qualifications
    {
      "institution": "string | null",    // Name of the university/college/institution
      "degree": "string | null",         // Degree obtained (e.g., "B.S.", "Master of Science")
      "major": "string | null",          // Field of study (e.g., "Computer Science")
      "location": "string | null",       // City, State of the institution
      "start_date": "string | null",     // Start date or year
      "end_date": "string | null",       // End date, graduation date, or expected graduation date
      "details": "string | null"         // Optional: GPA, Honors, relevant coursework, thesis title etc.
    }
  ],
  "skills": ["string"],                   // Comprehensive list of skills (technical, soft, tools, programming languages, frameworks, databases, etc.)
  "projects": [                          // List of personal or academic projects
     {
       "name": "string | null",          // Project name
       "description": "string | null",   // Brief description of the project
       "technologies_used": ["string"],  // List of key technologies/tools used
       "link": "string | null"           // URL to the project (e.g., GitHub repo, live demo)
     }
  ],
  "certifications": ["string"],           // List of relevant certifications (e.g., "AWS Certified Solutions Architect")
  "languages": ["string"],                // List of spoken/written languages and proficiency (e.g., "English (Native)", "Spanish (Fluent)")
  "awards_and_honors": ["string"]         // List of significant awards or honors
}
"""


# --- Core Functions ---

def load_api_key():
    """Loads the Google API key from environment variables."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logging.error("Error: GOOGLE_API_KEY environment variable not set.")
        sys.exit("Please set the GOOGLE_API_KEY environment variable.")
    return api_key


def extract_text_from_pdf(file_path):
    """Extracts text content from a PDF file."""
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() or ""  # Add safety for empty pages
            logging.info(f"Successfully extracted text from PDF: {file_path}")
            return text
    except FileNotFoundError:
        logging.error(f"Error: PDF file not found at {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading PDF file {file_path}: {e}")
        return None


def extract_text_from_docx(file_path):
    """Extracts text content from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        logging.info(f"Successfully extracted text from DOCX: {file_path}")
        return text
    except FileNotFoundError:
        logging.error(f"Error: DOCX file not found at {file_path}")
        return None
    except Exception as e:
        # Catch potential errors from python-docx (e.g., corrupted file)
        logging.error(f"Error reading DOCX file {file_path}: {e}")
        return None


def get_resume_text(file_path):
    """Detects file type and extracts text."""
    if not os.path.exists(file_path):
        logging.error(f"Error: File does not exist at {file_path}")
        return None

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.doc':
        logging.warning(
            f"Warning: '.doc' files are not directly supported. Please convert '{os.path.basename(file_path)}' to PDF or DOCX.")
        return None
    else:
        logging.error(f"Error: Unsupported file type '{file_extension}'. Please provide a PDF or DOCX file.")
        return None


def build_gemini_prompt(resume_text, schema_definition):
    """Constructs the prompt for the Gemini model."""

    prompt = f"""
    Analyze the following resume text and extract the key information precisely according to the JSON schema provided below.

    **Instructions:**
    1. Parse the entire resume text carefully.
    2. Populate the JSON object based *only* on the information present in the text.
    3. Adhere *strictly* to the specified JSON schema structure and field names.
    4. For fields where information is not found in the resume, use `null` for string types and empty lists `[]` for array types.
    5. Combine bullet points or multiple lines related to a single description (like job responsibilities) into a single string field, perhaps using newline characters if appropriate within the JSON string.
    6. Ensure the output is a single, valid JSON object *only*. Do not include any introductory text, explanations, apologies, markdown formatting (like ```json), or any text outside the JSON structure itself.

    **JSON Schema to Follow:**
    ```json
    {schema_definition.strip()}
    ```

    **Resume Text:**
    --- START RESUME ---
    {resume_text}
    --- END RESUME ---

    **Output (JSON only):**
    """
    return prompt.strip()


def call_gemini_flash(prompt, api_key):
    """Calls the Gemini Flash API to extract information."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=GEMINI_MODEL_NAME,
            safety_settings=SAFETY_SETTINGS,
            generation_config=GENERATION_CONFIG
        )
        logging.info("Sending request to Gemini API...")
        response = model.generate_content(prompt)

        # Debug: Print raw response text before JSON parsing
        # logging.debug(f"Raw Gemini Response Text:\n{response.text}")

        # Directly use response.text as it should be JSON formatted
        # due to response_mime_type="application/json"
        json_response_text = response.text

        # Attempt to parse the cleaned text as JSON
        try:
            parsed_json = json.loads(json_response_text)
            logging.info("Successfully parsed Gemini response as JSON.")
            return parsed_json
        except json.JSONDecodeError as json_err:
            logging.error(f"Error: Failed to decode Gemini response into JSON.")
            logging.error(f"JSON Decode Error: {json_err}")
            logging.error(f"Received text (first 500 chars): {json_response_text[:500]}...")
            # Fallback: Try to extract JSON block if markdown was accidentally included
            try:
                logging.warning("Attempting fallback JSON extraction...")
                json_block = json_response_text.split('```json\n', 1)[1].split('\n```', 1)[0]
                parsed_json = json.loads(json_block)
                logging.info("Successfully parsed Gemini response using fallback JSON extraction.")
                return parsed_json
            except Exception as fallback_err:
                logging.error(f"Fallback JSON extraction failed: {fallback_err}")
                return None

    except AttributeError:
        # Handle cases where the response might be blocked or have no text
        logging.error(
            "Error: Could not access Gemini response text. The request might have been blocked due to safety settings or other issues.")
        try:
            logging.error(f"Prompt Feedback: {response.prompt_feedback}")
        except Exception:
            pass  # Ignore if prompt_feedback is not available
        return None
    except Exception as e:
        logging.error(f"An error occurred during the Gemini API call: {e}")
        # Log specific details if available (e.g., from google.api_core.exceptions)
        if hasattr(e, 'message'):
            logging.error(f"API Error Message: {e.message}")
        return None

def parse_resume(resume_path):
    print("Parsing resume...", resume_path)
    parser = argparse.ArgumentParser(
        description="Extract information from PDF or DOCX resumes into JSON using Gemini Flash.")
    parser.add_argument("resume_path", help="Path to the resume file (PDF or DOCX).")
    parser.add_argument("-o", "--output", help="Optional path to save the output JSON file.", default=None)
    parser.add_argument("-d", "--debug", help="Enable debug logging.", action="store_true")
    # 1. Load API Key
    api_key = load_api_key()

    # 2. Extract Text from Resume
    logging.info(f"Processing resume: {resume_path}")
    resume_text = get_resume_text(resume_path)
    if not resume_text:
        sys.exit(1)  # Exit if text extraction failed

    if len(resume_text.strip()) < 50:  # Basic check for meaningful content
        logging.warning("Warning: Extracted text seems very short. Parsing might be inaccurate.")

    # 3. Build Prompt
    prompt = build_gemini_prompt(resume_text, JSON_SCHEMA_DEFINITION)
    logging.debug(f"Constructed Prompt (first 500 chars):\n{prompt[:500]}...")

    # 4. Call Gemini API
    extracted_data = call_gemini_flash(prompt, api_key)

    # 5. Output Results
    if extracted_data:
        logging.info("Successfully extracted resume data.")
        return extracted_data
    else:
        logging.error("Failed to extract resume data.")
