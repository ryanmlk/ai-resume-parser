from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

class KeywordExtractor:
    def __init__(self, max_features=100, min_df=2):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            min_df=min_df,
            stop_words='english',
            ngram_range=(1, 2)  # Allow for single words and bi-grams
        )
        
    def extract_keywords(self, texts):
        # Fit and transform the texts
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get keywords for each document
        keywords_by_doc = {}
        for idx, text in enumerate(texts):
            # Get scores for this document
            doc_scores = tfidf_matrix[idx].toarray()[0]
            # Get indices of top scoring terms
            top_indices = np.argsort(doc_scores)[-10:][::-1]  # Get top 10 keywords
            # Map indices to terms and scores
            keywords = {
                feature_names[i]: float(doc_scores[i]) 
                for i in top_indices 
                if doc_scores[i] > 0
            }
            keywords_by_doc[text] = keywords
            
        return keywords_by_doc

def main():
    # Read the parsed job descriptions
    df = pd.read_csv('data/processed/parsed_jobs.csv', 
                     names=['skills', 'experience_level', 'raw_text'])
    
    # Initialize extractor
    extractor = KeywordExtractor(max_features=200, min_df=2)
    
    # Extract keywords from raw text
    keywords_dict = extractor.extract_keywords(df['raw_text'].tolist())
    
    # Convert results to DataFrame
    results = []
    for text, keywords in keywords_dict.items():
        row = {
            'text': text,
            'keywords': ', '.join(keywords.keys()),
            'keyword_scores': ', '.join(f"{k}:{v:.3f}" for k, v in keywords.items())
        }
        results.append(row)
    
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv('data/processed/extracted_keywords.csv', index=False)

if __name__ == "__main__":
    main() 