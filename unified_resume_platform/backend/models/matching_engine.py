# matching_engine.py
import numpy as np
import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

# Download required NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

class ResumeMatcher:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if not text:
            return ""
            
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and short tokens
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        # Lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return ' '.join(tokens)
    
    def extract_skills(self, text):
        """Extract potential skills from text"""
        # Common skills database (in a real app, this would be more comprehensive)
        common_skills = {
            'python', 'java', 'javascript', 'sql', 'html', 'css', 'react', 'angular',
            'nodejs', 'django', 'flask', 'aws', 'docker', 'kubernetes', 'git',
            'machine learning', 'data analysis', 'project management', 'agile',
            'scrum', 'rest api', 'mongodb', 'mysql', 'postgresql', 'linux',
            'excel', 'power bi', 'tableau', 'tensorflow', 'pytorch', 'pandas',
            'numpy', 'scikit-learn', 'ci/cd', 'jenkins', 'azure', 'gcp'
        }
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
                
        return found_skills
    
    def calculate_match_score(self, resume_text, job_description):
        """Calculate match score between resume and job description"""
        # Preprocess texts
        processed_resume = self.preprocess_text(resume_text)
        processed_jd = self.preprocess_text(job_description)
        
        if not processed_resume or not processed_jd:
            return 0.0, [], []
        
        # Create TF-IDF vectors
        try:
            tfidf_matrix = self.vectorizer.fit_transform([processed_resume, processed_jd])
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            match_score = similarity_matrix[0][0] * 100
            
            # Extract skills from both documents
            resume_skills = self.extract_skills(resume_text)
            jd_skills = self.extract_skills(job_description)
            
            # Calculate skill match
            if jd_skills:
                skill_match_ratio = len(set(resume_skills) & set(jd_skills)) / len(jd_skills) * 100
            else:
                skill_match_ratio = 0
            
            final_score = (match_score * 0.3) + (skill_match_ratio * 0.7)
            
            return final_score, resume_skills, jd_skills
            
        except Exception as e:
            print(f"Error calculating match score: {e}")
            return 0.0, [], []
    
    def get_match_analysis(self, resume_text, job_description):
        """Get detailed match analysis"""
        score, resume_skills, jd_skills = self.calculate_match_score(resume_text, job_description)
        
        # Find matching and missing skills
        matching_skills = set(resume_skills) & set(jd_skills)
        missing_skills = set(jd_skills) - set(resume_skills)
        
        analysis = {
            'match_score': round(score, 2),
            'resume_skills': list(resume_skills),
            'jd_skills': list(jd_skills),
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'skill_match_percentage': round((len(matching_skills) / len(jd_skills) * 100) if jd_skills else 0, 2)
        }
        
        return analysis