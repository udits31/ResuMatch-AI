"""
Job Analyzer - Extracts keywords and requirements from job descriptions
"""

import re
from typing import Dict, List, Set, Any
from collections import Counter
from .skill_extractor import get_skill_extractor


class JobAnalyzer:
    """Analyzes job descriptions to extract key requirements and keywords"""
    
    def __init__(self):
        """Initialize JobAnalyzer with common patterns and stopwords"""
        self.skill_extractor = get_skill_extractor()
        self.skill_patterns = [
            r'\b(?:python|java|javascript|c\+\+|c#|sql|html|css|react|angular|vue|node\.?js)\b',
            r'\b(?:aws|azure|gcp|docker|kubernetes|git|jenkins|terraform)\b',
            r'\b(?:machine learning|data science|artificial intelligence|ai|ml)\b',
            r'\b(?:agile|scrum|devops|ci/cd|microservices|rest|api)\b'
        ]
        
        self.experience_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:minimum|min|at least)\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)-(\d+)\s*(?:years?|yrs?)'
        ]
        
        self.education_patterns = [
            r'\b(?:bachelor|bs|ba|master|ms|ma|phd|doctorate)\b',
            r'\b(?:degree|diploma|certification)\b',
            r'\b(?:computer science|engineering|mathematics|statistics)\b'
        ]
        
        self.stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
    
    def extract_keywords(self, job_description: str) -> List[str]:
        """Extract relevant keywords from job description"""
        if not job_description or not job_description.strip():
            return []
        
        # Convert to lowercase for processing
        text = job_description.lower()
        
        technical_keywords = []
        for pattern in self.skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            technical_keywords.extend(matches)
        
        # Remove punctuation and split into words
        cleaned_text = re.sub(r'[^\w\s]', ' ', text)
        words = cleaned_text.split()
        
        # Filter out stopwords and short words
        filtered_words = [
            word for word in words 
            if len(word) > 2 and word not in self.stopwords
        ]
        
        # Extract 2-3 word phrases
        phrases = []
        for i in range(len(filtered_words) - 1):
            two_word = f"{filtered_words[i]} {filtered_words[i+1]}"
            phrases.append(two_word)
            
            if i < len(filtered_words) - 2:
                three_word = f"{filtered_words[i]} {filtered_words[i+1]} {filtered_words[i+2]}"
                phrases.append(three_word)
        
        all_keywords = technical_keywords + filtered_words + phrases
        
        keyword_counts = Counter(all_keywords)
        
        return [keyword for keyword, count in keyword_counts.most_common(20)]
    
    def identify_requirements(self, job_description: str) -> Dict[str, Any]:
        """Identify specific requirements from job description"""
        if not job_description or not job_description.strip():
            return {
                "required_skills": [],
                "preferred_skills": [],
                "experience_level": "",
                "education_requirements": "",
                "key_responsibilities": [],
                "company_info": ""
            }
        
        text = job_description.lower()
        
        # Extract required vs preferred skills
        required_skills = []
        preferred_skills = []
        
        # Look for required skills sections
        required_sections = re.findall(
            r'(?:required|must have|essential).*?(?:preferred|nice to have|plus|bonus|\n\n)',
            text, re.DOTALL
        )
        
        for section in required_sections:
            required_skills.extend(self.skill_extractor.extract(section))

        # Look for preferred skills sections
        preferred_sections = re.findall(
            r'(?:preferred|nice to have|plus|bonus|would be great).*?(?:\n\n|$)',
            text, re.DOTALL
        )

        for section in preferred_sections:
            preferred_skills.extend(self.skill_extractor.extract(section))

        # Fallback: if no explicit sections were found, treat all detected skills as required
        if not required_skills and not preferred_skills:
            required_skills = self.skill_extractor.extract(job_description)

        # Don't list a skill as preferred if it is already required
        preferred_skills = [s for s in preferred_skills if s not in set(required_skills)]
        
        # Extract experience level
        experience_level = ""
        for pattern in self.experience_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 1:
                    experience_level = f"{match.group(1)} years"
                elif len(match.groups()) == 2:
                    experience_level = f"{match.group(1)}-{match.group(2)} years"
                break
        
        # Additional pattern for "3+ years" format
        if not experience_level:
            plus_pattern = r'(\d+)\+\s*(?:years?|yrs?)'
            match = re.search(plus_pattern, text, re.IGNORECASE)
            if match:
                experience_level = f"{match.group(1)}+ years"
        
        # Extract education requirements
        education_requirements = ""
        for pattern in self.education_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                education_requirements = match.group(0)
                break
        
        # Extract key responsibilities (look for bullet points or numbered lists)
        responsibilities = []
        responsibility_patterns = [
            r'(?:•|\*|-|\d+\.)\s*([^\n•\*\-\d]+)',
            r'(?:responsibilities|duties).*?(?:\n\n|requirements)',
        ]
        
        for pattern in responsibility_patterns:
            matches = re.findall(pattern, job_description, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if len(match.strip()) > 20:  # Filter out short matches
                    responsibilities.append(match.strip())
        
        # Extract company info (first paragraph usually)
        company_info = ""
        paragraphs = job_description.split('\n\n')
        if paragraphs:
            company_info = paragraphs[0][:200] + "..." if len(paragraphs[0]) > 200 else paragraphs[0]
        
        return {
            "required_skills": list(set(required_skills)),
            "preferred_skills": list(set(preferred_skills)),
            "experience_level": experience_level,
            "education_requirements": education_requirements,
            "key_responsibilities": responsibilities[:5],  # Top 5 responsibilities
            "company_info": company_info
        }
    
    def calculate_relevance_score(self, profile: Dict[str, Any], job_requirements: Dict[str, Any]) -> float:
        """Calculate how well a profile matches job requirements"""
        if not profile or not job_requirements:
            return 0.0
        
        total_score = 0.0
        max_score = 0.0
        
        # Score technical skills match (40% weight)
        profile_skills = []
        if "skills" in profile:
            skills = profile["skills"]
            if isinstance(skills, dict):
                for skill_type in ["technical", "soft", "languages", "certifications"]:
                    if skill_type in skills and isinstance(skills[skill_type], list):
                        profile_skills.extend([skill.lower() for skill in skills[skill_type]])
        
        required_skills = [skill.lower() for skill in job_requirements.get("required_skills", [])]
        preferred_skills = [skill.lower() for skill in job_requirements.get("preferred_skills", [])]
        
        skills_score = 0.0
        skills_max = 40.0
        
        if required_skills:
            required_matches = sum(1 for skill in required_skills if any(skill in ps for ps in profile_skills))
            skills_score += (required_matches / len(required_skills)) * 30.0
        
        if preferred_skills:
            preferred_matches = sum(1 for skill in preferred_skills if any(skill in ps for ps in profile_skills))
            skills_score += (preferred_matches / len(preferred_skills)) * 10.0
        
        total_score += skills_score
        max_score += skills_max
        
        # Score experience level match (30% weight)
        experience_score = 0.0
        experience_max = 30.0
        
        if "work_experience" in profile and isinstance(profile["work_experience"], list):
            total_experience = len(profile["work_experience"])
            
            # Extract required years from job requirements
            exp_requirement = job_requirements.get("experience_level", "")
            required_years = 0
            
            if exp_requirement:
                years_match = re.search(r'(\d+)', exp_requirement)
                if years_match:
                    required_years = int(years_match.group(1))
            
            if required_years > 0:
                if total_experience >= required_years:
                    experience_score = experience_max
                else:
                    experience_score = (total_experience / required_years) * experience_max
            else:
                experience_score = experience_max * 0.5  # Default score if no requirement
        
        total_score += experience_score
        max_score += experience_max
        
        # Score education match (20% weight)
        education_score = 0.0
        education_max = 20.0
        
        if "education" in profile and isinstance(profile["education"], list):
            profile_education = [edu.get("degree", "").lower() for edu in profile["education"]]
            job_education = job_requirements.get("education_requirements", "").lower()
            
            if job_education:
                if any(edu in job_education for edu in profile_education if edu):
                    education_score = education_max
                else:
                    education_score = education_max * 0.3  # Partial credit
            else:
                education_score = education_max * 0.5  # Default if no requirement
        
        total_score += education_score
        max_score += education_max
        
        # Score summary/description relevance (10% weight)
        summary_score = 0.0
        summary_max = 10.0
        
        profile_text = ""
        if "summary" in profile:
            profile_text += profile["summary"].lower()
        
        # Add work experience descriptions
        if "work_experience" in profile:
            for exp in profile["work_experience"]:
                if "description" in exp:
                    profile_text += " " + exp["description"].lower()
        
        if profile_text and required_skills:
            matches = sum(1 for skill in required_skills if skill in profile_text)
            summary_score = (matches / len(required_skills)) * summary_max
        
        total_score += summary_score
        max_score += summary_max
        
        # Return normalized score
        return min(total_score / max_score, 1.0) if max_score > 0 else 0.0