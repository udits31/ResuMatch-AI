"""
Resume Generator - Creates tailored resumes based on profile and job analysis
"""

from typing import Dict, List, Any, Tuple
import re
from datetime import datetime


class ResumeGenerator:
    """Generates tailored resumes matching profile data with job requirements"""
    
    def __init__(self):
        """Initialize ResumeGenerator with formatting settings"""
        self.max_lines = 50  # Approximate lines for 1-2 pages
        self.section_priorities = {
            "personal_info": 1,
            "summary": 2,
            "work_experience": 3,
            "skills": 4,
            "education": 5,
            "projects": 6
        }
    
    def generate_resume(self, profile: Dict[str, Any], job_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a tailored resume based on profile and job analysis"""
        if not profile:
            raise ValueError("Profile data is required")
        
        # Prioritize content based on job relevance
        prioritized_content = self.prioritize_content(profile, job_analysis.get("required_skills", []))
        
        # Generate tailored sections
        resume_data = {
            "personal_info": self._generate_personal_info(prioritized_content.get("personal_info", {})),
            "summary": self._generate_tailored_summary(
                prioritized_content.get("summary", ""),
                job_analysis
            ),
            "work_experience": self._generate_work_experience(
                prioritized_content.get("work_experience", []),
                job_analysis
            ),
            "skills": self._generate_skills_section(
                prioritized_content.get("skills", {}),
                job_analysis
            ),
            "education": self._generate_education_section(
                prioritized_content.get("education", [])
            ),
            "projects": self._generate_projects_section(
                prioritized_content.get("projects", []),
                job_analysis
            ),
            "publications": prioritized_content.get("publications", []),
            "extracurricular": prioritized_content.get("extracurricular", [])
        }
        
        # Ensure resume fits within page limits
        resume_data = self._optimize_length(resume_data)
        
        return resume_data
    
    def prioritize_content(self, profile: Dict[str, Any], job_keywords: List[str]) -> Dict[str, Any]:
        """Prioritize profile content based on job relevance"""
        if not profile:
            return {}
        
        job_keywords_lower = [keyword.lower() for keyword in job_keywords]
        prioritized_profile = profile.copy()
        
        # Prioritize work experience by relevance
        if "work_experience" in profile and isinstance(profile["work_experience"], list):
            work_exp = profile["work_experience"].copy()
            
            # Score each work experience
            for exp in work_exp:
                exp["_relevance_score"] = self._calculate_experience_relevance(exp, job_keywords_lower)
            
            # Sort by relevance score (descending) and recency
            work_exp.sort(key=lambda x: (x.get("_relevance_score", 0), x.get("start_date", "")), reverse=True)
            
            # Remove scoring field
            for exp in work_exp:
                exp.pop("_relevance_score", None)
            
            prioritized_profile["work_experience"] = work_exp
        
        # Prioritize skills by relevance
        if "skills" in profile and isinstance(profile["skills"], dict):
            skills = profile["skills"].copy()
            
            for skill_type in skills:
                if isinstance(skills[skill_type], list):
                    skill_list = skills[skill_type].copy()
                    
                    # Score and sort skills
                    scored_skills = []
                    for skill in skill_list:
                        score = self._calculate_skill_relevance(skill, job_keywords_lower)
                        scored_skills.append((skill, score))
                    
                    scored_skills.sort(key=lambda x: x[1], reverse=True)
                    skills[skill_type] = [skill for skill, score in scored_skills]
            
            prioritized_profile["skills"] = skills
        
        # Prioritize projects by relevance
        if "projects" in profile and isinstance(profile["projects"], list):
            projects = profile["projects"].copy()
            
            for project in projects:
                project["_relevance_score"] = self._calculate_project_relevance(project, job_keywords_lower)
            
            projects.sort(key=lambda x: x.get("_relevance_score", 0), reverse=True)
            
            # Remove scoring field
            for project in projects:
                project.pop("_relevance_score", None)
            
            prioritized_profile["projects"] = projects
        
        return prioritized_profile
    
    def format_resume(self, resume_data: Dict[str, Any]) -> str:
        """Format resume data into a professional text format"""
        if not resume_data:
            return ""
        
        formatted_sections = []
        
        # Personal Information
        personal_info = resume_data.get("personal_info", {})
        if personal_info:
            header = []
            if personal_info.get("name"):
                header.append(personal_info["name"].upper())
            if personal_info.get("headline"):
                header.append(personal_info["headline"])

            contact_info = []
            for field in ["email", "phone", "location", "address", "linkedin"]:
                if personal_info.get(field):
                    contact_info.append(personal_info[field])
            
            if contact_info:
                header.append(" | ".join(contact_info))
            
            if header:
                formatted_sections.append("\n".join(header))
                formatted_sections.append("=" * 60)
        
        # Summary
        summary = resume_data.get("summary", "")
        if summary:
            formatted_sections.append("PROFESSIONAL SUMMARY")
            formatted_sections.append("-" * 20)
            formatted_sections.append(summary)

                # Education
        education = resume_data.get("education", [])
        if education:
            formatted_sections.append("EDUCATION")
            formatted_sections.append("-" * 9)
            
            for edu in education:
                edu_lines = []
                
                # Degree and Field
                degree_line = ""
                if edu.get("degree"):
                    degree_line = edu["degree"]
                if edu.get("field"):
                    degree_line += f" in {edu['field']}"
                if degree_line:
                    edu_lines.append(degree_line)
                
                # Institution and Date
                inst_line = ""
                if edu.get("institution"):
                    inst_line = edu["institution"]
                if edu.get("graduation_date"):
                    inst_line += f" | {edu['graduation_date']}"
                if inst_line:
                    edu_lines.append(inst_line)
                
                # GPA (if notable)
                if edu.get("gpa") and edu["gpa"] >= 3.5:
                    edu_lines.append(f"GPA: {edu['gpa']}")
                
                if edu_lines:
                    formatted_sections.append("\n".join(edu_lines))
        
        # Work Experience
        work_exp = resume_data.get("work_experience", [])
        if work_exp:
            formatted_sections.append("WORK EXPERIENCE")
            formatted_sections.append("-" * 15)
            
            for exp in work_exp:
                exp_lines = []
                
                # Position and Company
                position_line = ""
                if exp.get("position"):
                    position_line = exp["position"]
                if exp.get("company"):
                    position_line += f" | {exp['company']}"
                if position_line:
                    exp_lines.append(position_line)
                
                # Dates
                date_line = ""
                if exp.get("start_date"):
                    date_line = exp["start_date"]
                    if exp.get("end_date"):
                        date_line += f" - {exp['end_date']}"
                    else:
                        date_line += " - Present"
                if date_line:
                    exp_lines.append(date_line)
                
                # Description
                if exp.get("description"):
                    exp_lines.append(f"• {exp['description']}")
                
                # Achievements
                achievements = exp.get("achievements", [])
                for achievement in achievements[:3]:  # Limit to top 3
                    exp_lines.append(f"• {achievement}")
                
                if exp_lines:
                    formatted_sections.append("\n".join(exp_lines))
        
        # Skills
        skills = resume_data.get("skills", {})
        if skills:
            formatted_sections.append("SKILLS")
            formatted_sections.append("-" * 6)
            
            for skill_type, skill_list in skills.items():
                if skill_list:
                    skill_type_formatted = skill_type.replace("_", " ").title()
                    skills_text = ", ".join(skill_list[:8])  # Limit to top 8 skills
                    formatted_sections.append(f"{skill_type_formatted}: {skills_text}")
              
        # Projects
        projects = resume_data.get("projects", [])
        if projects:
            formatted_sections.append("PROJECTS")
            formatted_sections.append("-" * 8)
            
            for project in projects[:3]:  # Limit to top 3 projects
                project_lines = []
                
                if project.get("name"):
                    project_lines.append(project["name"])
                
                if project.get("description"):
                    project_lines.append(f"• {project['description']}")
                
                if project.get("technologies"):
                    tech_list = ", ".join(project["technologies"][:5])
                    project_lines.append(f"Technologies: {tech_list}")
                
                if project.get("url"):
                    project_lines.append(f"URL: {project['url']}")
                
                if project_lines:
                    formatted_sections.append("\n".join(project_lines))

        # Publications
        publications = resume_data.get("publications", [])
        if publications:
            formatted_sections.append("PUBLICATIONS")
            formatted_sections.append("-" * 12)
            for pub in publications:
                pub_lines = []
                title_line = pub.get("title", "")
                if pub.get("venue"):
                    title_line += f" | {pub['venue']}"
                if title_line:
                    pub_lines.append(title_line)
                if pub.get("description"):
                    pub_lines.append(f"• {pub['description']}")
                if pub.get("url"):
                    pub_lines.append(pub["url"])
                if pub_lines:
                    formatted_sections.append("\n".join(pub_lines))

        # Extra-curricular / Leadership
        extracurricular = resume_data.get("extracurricular", [])
        if extracurricular:
            formatted_sections.append("EXTRA-CURRICULAR / LEADERSHIP")
            formatted_sections.append("-" * 28)
            for act in extracurricular:
                act_lines = []
                title_line = act.get("title", "")
                if act.get("organization"):
                    title_line += f" | {act['organization']}"
                if title_line:
                    act_lines.append(title_line)
                if act.get("description"):
                    act_lines.append(f"• {act['description']}")
                if act_lines:
                    formatted_sections.append("\n".join(act_lines))

        return "\n\n".join(formatted_sections)
    
    def _generate_personal_info(self, personal_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personal information section"""
        return {
            "name": personal_info.get("name", ""),
            "email": personal_info.get("email", ""),
            "phone": personal_info.get("phone", ""),
            "address": personal_info.get("address", ""),
            "linkedin": personal_info.get("linkedin", ""),
            "headline": personal_info.get("headline", ""),
            "location": personal_info.get("location", "")
        }
    
    def _generate_tailored_summary(self, original_summary: str, job_analysis: Dict[str, Any]) -> str:
        """Generate a tailored professional summary"""
        if not original_summary:
            return ""
        
        # Extract key skills from job requirements
        required_skills = job_analysis.get("required_skills", [])
        preferred_skills = job_analysis.get("preferred_skills", [])
        all_job_skills = required_skills + preferred_skills
        
        # Enhance summary with relevant keywords
        enhanced_summary = original_summary
        
        # Add relevant skills if not already mentioned
        summary_lower = original_summary.lower()
        missing_skills = [skill for skill in all_job_skills[:3] if skill.lower() not in summary_lower]
        
        if missing_skills:
            skills_text = ", ".join(missing_skills)
            enhanced_summary += f" Experienced with {skills_text}."
        
        return enhanced_summary
    
    def _generate_work_experience(self, work_experience: List[Dict[str, Any]], job_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate tailored work experience section"""
        if not work_experience:
            return []
        
        job_keywords = job_analysis.get("required_skills", []) + job_analysis.get("preferred_skills", [])
        
        tailored_experience = []
        for exp in work_experience[:4]:  # Limit to top 4 experiences
            tailored_exp = exp.copy()
            
            # Enhance description with relevant keywords
            if "description" in exp and job_keywords:
                enhanced_desc = self._enhance_description(exp["description"], job_keywords)
                tailored_exp["description"] = enhanced_desc
            
            tailored_experience.append(tailored_exp)
        
        return tailored_experience
    
    def _generate_skills_section(self, skills: Dict[str, List[str]], job_analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate tailored skills section"""
        if not skills:
            return {}
        
        job_skills = job_analysis.get("required_skills", []) + job_analysis.get("preferred_skills", [])
        job_skills_lower = [skill.lower() for skill in job_skills]
        
        tailored_skills = {}
        
        for skill_type, skill_list in skills.items():
            if not skill_list:
                continue
            
            # Prioritize skills that match job requirements
            prioritized_skills = []
            other_skills = []
            
            for skill in skill_list:
                if any(job_skill in skill.lower() for job_skill in job_skills_lower):
                    prioritized_skills.append(skill)
                else:
                    other_skills.append(skill)
            
            # Combine prioritized skills first, then others
            combined_skills = prioritized_skills + other_skills
            tailored_skills[skill_type] = combined_skills[:10]  # Limit to top 10
        
        return tailored_skills
    
    def _generate_education_section(self, education: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate education section"""
        return education[:3] if education else []  # Limit to top 3
    
    def _generate_projects_section(self, projects: List[Dict[str, Any]], job_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate tailored projects section"""
        if not projects:
            return []
        
        # Return top 3 most relevant projects (already prioritized)
        return projects[:3]
    
    def _calculate_experience_relevance(self, experience: Dict[str, Any], job_keywords: List[str]) -> float:
        """Calculate relevance score for work experience"""
        score = 0.0
        
        # Check description for keyword matches
        description = experience.get("description", "").lower()
        for keyword in job_keywords:
            if keyword in description:
                score += 1.0
        
        # Check achievements for keyword matches
        achievements = experience.get("achievements", [])
        for achievement in achievements:
            achievement_lower = achievement.lower()
            for keyword in job_keywords:
                if keyword in achievement_lower:
                    score += 0.5
        
        # Bonus for recent experience
        start_date = experience.get("start_date", "")
        if start_date:
            try:
                # Simple year extraction
                year_match = re.search(r'\d{4}', start_date)
                if year_match:
                    year = int(year_match.group())
                    current_year = datetime.now().year
                    if current_year - year <= 3:  # Recent experience
                        score += 1.0
            except:
                pass
        
        return score
    
    def _calculate_skill_relevance(self, skill: str, job_keywords: List[str]) -> float:
        """Calculate relevance score for a skill"""
        skill_lower = skill.lower()
        for keyword in job_keywords:
            if keyword in skill_lower or skill_lower in keyword:
                return 1.0
        return 0.0
    
    def _calculate_project_relevance(self, project: Dict[str, Any], job_keywords: List[str]) -> float:
        """Calculate relevance score for a project"""
        score = 0.0
        
        # Check description
        description = project.get("description", "").lower()
        for keyword in job_keywords:
            if keyword in description:
                score += 1.0
        
        # Check technologies
        technologies = project.get("technologies", [])
        for tech in technologies:
            tech_lower = tech.lower()
            for keyword in job_keywords:
                if keyword in tech_lower:
                    score += 0.5
        
        return score
    
    def _enhance_description(self, description: str, job_keywords: List[str]) -> str:
        """Enhance description with relevant keywords"""
        if not description or not job_keywords:
            return description
        
        # Simple enhancement - ensure key skills are mentioned
        enhanced = description
        description_lower = description.lower()
        
        # Add missing relevant keywords naturally
        missing_keywords = [kw for kw in job_keywords[:2] if kw.lower() not in description_lower]
        
        if missing_keywords:
            keywords_text = ", ".join(missing_keywords)
            enhanced += f" Utilized {keywords_text} to achieve results."
        
        return enhanced
    
    def _optimize_length(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize resume length to fit within page limits"""
        # Estimate current length
        formatted_text = self.format_resume(resume_data)
        current_lines = len(formatted_text.split('\n'))
        
        if current_lines <= self.max_lines:
            return resume_data
        
        # Reduce content to fit
        optimized_data = resume_data.copy()
        
        # Reduce work experience
        if "work_experience" in optimized_data:
            work_exp = optimized_data["work_experience"]
            if len(work_exp) > 3:
                optimized_data["work_experience"] = work_exp[:3]
        
        # Reduce projects
        if "projects" in optimized_data:
            projects = optimized_data["projects"]
            if len(projects) > 2:
                optimized_data["projects"] = projects[:2]
        
        # Reduce achievements per job
        if "work_experience" in optimized_data:
            for exp in optimized_data["work_experience"]:
                if "achievements" in exp and len(exp["achievements"]) > 2:
                    exp["achievements"] = exp["achievements"][:2]
        
        return optimized_data