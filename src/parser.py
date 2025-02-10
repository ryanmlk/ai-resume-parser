import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class JobDescriptionParser:
    def __init__(self):
        # Load spaCy English model
        self.nlp = spacy.load("en_core_web_sm")
        
    def preprocess_text(self, text):
        """Clean and normalize job description text"""
        # Remove HTML tags
        text = re.sub('<.*?>', '', text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def extract_key_skills(self, text):
        """Extract skills from job description"""
        doc = self.nlp(text)
        skills = []
        
        # Define skill-related patterns
        skill_patterns = [
            'python', 'java', 'machine learning', 
            'data analysis', 'communication', 'leadership'
        ]
        
        for ent in doc.ents:
            if ent.label_ in ['PRODUCT', 'ORG']:
                skills.append(ent.text)
        
        # Manual skill matching
        for pattern in skill_patterns:
            if pattern in text:
                skills.append(pattern)
        
        return list(set(skills))
    
    def classify_experience_level(self, text):
        """Determine job experience level"""
        experience_keywords = {
            'entry': ['junior', 'entry', 'associate', 'starter'],
            'mid': ['mid', 'intermediate', 'senior'],
            'expert': ['expert', 'principal', 'lead', 'director']
        }
        
        text = text.lower()
        for level, keywords in experience_keywords.items():
            if any(keyword in text for keyword in keywords):
                return level
        
        return 'not specified'
    
    def parse_job_description(self, job_description):
        """Main parsing method"""
        cleaned_text = self.preprocess_text(job_description)
        
        return {
            'skills': self.extract_key_skills(cleaned_text),
            'experience_level': self.classify_experience_level(cleaned_text),
            'raw_text': cleaned_text
        }

parser = JobDescriptionParser()
job_listings = pd.read_csv("data/raw/job-sample.csv")
for job_description in job_listings["job_description"]:
    parsed_result = parser.parse_job_description(job_description)
    # Create a DataFrame from parsed results and save to CSV
    parsed_results_df = pd.DataFrame([parsed_result])
    parsed_results_df.to_csv('data/processed/parsed_jobs.csv', mode='a', header=False, index=False)