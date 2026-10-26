# matching_engine.py
import os
# sentence-transformers runs on PyTorch. Stop the `transformers` library from
# importing TensorFlow/Flax, which otherwise fails here (Keras 3 without tf-keras).
# These must be set before `transformers` is first imported.
os.environ.setdefault("USE_TF", "0")
os.environ.setdefault("USE_FLAX", "0")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")

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

# ---------------------------------------------------------------------------
# Lazy-loaded semantic model (sentence-transformers / all-MiniLM-L6-v2).
# Loaded once on first use so app startup stays fast, and the whole app still
# works (falling back to TF-IDF) if the library/model isn't available.
# ---------------------------------------------------------------------------
_EMBED_MODEL = None
_EMBED_MODEL_TRIED = False

def _get_embedding_model():
    global _EMBED_MODEL, _EMBED_MODEL_TRIED
    if _EMBED_MODEL_TRIED:
        return _EMBED_MODEL
    _EMBED_MODEL_TRIED = True
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        model.max_seq_length = 512  # use more of each document than the 256 default
        _EMBED_MODEL = model
        print("[ok] Semantic model loaded (all-MiniLM-L6-v2)")
    except Exception as e:
        print(f"[warn] Semantic model unavailable, using TF-IDF only: {e}")
        _EMBED_MODEL = None
    return _EMBED_MODEL

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
    
    def calculate_tfidf_similarity(self, processed_resume, processed_jd):
        """Lexical (bag-of-words) similarity: TF-IDF vectors + cosine. Returns 0-100.

        This is the original matching method, kept as a baseline to compare the
        semantic model against.
        """
        if not processed_resume or not processed_jd:
            return 0.0
        try:
            tfidf_matrix = self.vectorizer.fit_transform([processed_resume, processed_jd])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity) * 100
        except Exception as e:
            print(f"Error computing TF-IDF similarity: {e}")
            return 0.0

    def calculate_semantic_similarity(self, resume_text, job_description):
        """Semantic similarity using sentence-embeddings + cosine. Returns 0-100,
        or None if the embedding model is unavailable (caller falls back to TF-IDF).

        Unlike TF-IDF, this captures meaning: e.g. "built REST APIs" and
        "API development" score as similar even without shared words. Raw text is
        used here (not the lemmatized/stopword-stripped text) because the model
        does its own tokenization and benefits from the original wording.
        """
        model = _get_embedding_model()
        if model is None or not resume_text or not job_description:
            return None
        try:
            embeddings = model.encode([resume_text, job_description], convert_to_numpy=True)
            a, b = embeddings[0], embeddings[1]
            denom = float(np.linalg.norm(a) * np.linalg.norm(b))
            if denom == 0:
                return 0.0
            similarity = float(np.dot(a, b) / denom)
            # cosine of embeddings can be slightly negative; clamp to [0, 1]
            similarity = max(0.0, min(1.0, similarity))
            return similarity * 100
        except Exception as e:
            print(f"Error computing semantic similarity: {e}")
            return None

    def get_match_analysis(self, resume_text, job_description):
        """Get detailed match analysis.

        Final score blends document similarity (30%) with skill overlap (70%).
        The document-similarity component prefers the semantic model when
        available and falls back to TF-IDF otherwise. Both raw scores are also
        returned so the UI can show semantic vs. TF-IDF side by side.
        """
        processed_resume = self.preprocess_text(resume_text)
        processed_jd = self.preprocess_text(job_description)

        tfidf_score = self.calculate_tfidf_similarity(processed_resume, processed_jd)
        semantic_score = self.calculate_semantic_similarity(resume_text, job_description)

        if semantic_score is not None:
            text_similarity = semantic_score
            method = 'semantic'
        else:
            text_similarity = tfidf_score
            method = 'tfidf'

        # Skill overlap
        resume_skills = self.extract_skills(resume_text)
        jd_skills = self.extract_skills(job_description)
        matching_skills = set(resume_skills) & set(jd_skills)
        missing_skills = set(jd_skills) - set(resume_skills)
        skill_match_ratio = (len(matching_skills) / len(jd_skills) * 100) if jd_skills else 0

        final_score = (text_similarity * 0.3) + (skill_match_ratio * 0.7)

        return {
            'match_score': round(final_score, 2),
            'semantic_score': round(semantic_score, 2) if semantic_score is not None else None,
            'tfidf_score': round(tfidf_score, 2),
            'similarity_method': method,
            'resume_skills': list(resume_skills),
            'jd_skills': list(jd_skills),
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'skill_match_percentage': round(skill_match_ratio, 2)
        }