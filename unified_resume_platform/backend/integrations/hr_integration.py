import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from psycopg2.extras import RealDictCursor

try:
    from ..models.matching_engine import ResumeMatcher
    from ..database.db_manager import DatabaseManager
except ImportError as e:
    print(f"Error importing HR modules: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    raise

class HRIntegration:
    def __init__(self):
        self.matcher = ResumeMatcher()
        self.db_manager = DatabaseManager()
    
    def get_resumes_from_db(self):
        """Fetch resumes for the dropdown, excluding auto-generated 'Analyzed Resume' entries"""
        try:
            if self.db_manager.connect():
                cursor = self.db_manager.connection.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT resume_id, resume_title, candidate_name, candidate_email FROM resumes WHERE NOT (resume_title = 'Analyzed Resume' AND candidate_name = 'Candidate') ORDER BY uploaded_at DESC")
                resumes = cursor.fetchall()
                cursor.close()
                self.db_manager.disconnect()
                return resumes
            return []
        except Exception as e:
            print(f"Error fetching resumes: {e}")
            return []
    
    def get_job_descriptions_from_db(self):
        """Fetch all job descriptions from database, excluding auto-generated 'Analyzed Job' entries"""
        try:
            if self.db_manager.connect():
                cursor = self.db_manager.connection.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT job_id, job_title, company_name FROM job_descriptions WHERE status = 'active' AND NOT (job_title = 'Analyzed Job' AND company_name = 'Company') ORDER BY posted_at DESC")
                job_descriptions = cursor.fetchall()
                cursor.close()
                self.db_manager.disconnect()
                return job_descriptions
            return []
        except Exception as e:
            print(f"Error fetching job descriptions: {e}")
            return []
    
    def get_resume_by_id(self, resume_id):
        """Fetch specific resume by ID"""
        try:
            if self.db_manager.connect():
                cursor = self.db_manager.connection.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT * FROM resumes WHERE resume_id = %s", (resume_id,))
                resume = cursor.fetchone()
                cursor.close()
                self.db_manager.disconnect()
                return resume
            return None
        except Exception as e:
            print(f"Error fetching resume: {e}")
            return None
    
    def get_job_description_by_id(self, job_id):
        """Fetch specific job description by ID"""
        try:
            if self.db_manager.connect():
                cursor = self.db_manager.connection.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT * FROM job_descriptions WHERE job_id = %s", (job_id,))
                job_description = cursor.fetchone()
                cursor.close()
                self.db_manager.disconnect()
                return job_description
            return None
        except Exception as e:
            print(f"Error fetching job description: {e}")
            return None

    def get_all_resumes_with_text(self):
        """Fetch all real resumes (id, title, name, full text), excluding analyzed entries"""
        try:
            if self.db_manager.connect():
                cursor = self.db_manager.connection.cursor(cursor_factory=RealDictCursor)
                cursor.execute("SELECT resume_id, resume_title, candidate_name, resume_text FROM resumes WHERE NOT (resume_title = 'Analyzed Resume' AND candidate_name = 'Candidate') ORDER BY resume_id")
                rows = cursor.fetchall()
                cursor.close()
                self.db_manager.disconnect()
                return rows
            return []
        except Exception as e:
            print(f"Error fetching resumes with text: {e}")
            return []

    def rank_candidates(self, job_description):
        """Score every resume in the database against one job description and return them ranked by match score"""
        try:
            if not job_description or not job_description.strip():
                return {'success': False, 'message': 'Job description is required', 'data': None, 'errors': ['Missing job description']}

            resumes = self.get_all_resumes_with_text()
            if not resumes:
                return {'success': False, 'message': 'No resumes available to rank', 'data': None, 'errors': ['No resumes in database']}

            ranked = []
            for r in resumes:
                analysis = self.matcher.get_match_analysis(r['resume_text'], job_description)
                ranked.append({
                    'resume_id': r['resume_id'],
                    'resume_title': r['resume_title'],
                    'candidate_name': r['candidate_name'],
                    'match_score': analysis['match_score'],
                    'semantic_score': analysis['semantic_score'],
                    'tfidf_score': analysis['tfidf_score'],
                    'skill_match_percentage': analysis['skill_match_percentage'],
                    'matching_skills': analysis['matching_skills'],
                    'missing_skills': analysis['missing_skills'],
                })

            ranked.sort(key=lambda c: c['match_score'], reverse=True)
            for i, c in enumerate(ranked, start=1):
                c['rank'] = i

            return {'success': True, 'message': f'Ranked {len(ranked)} candidates', 'data': {'candidates': ranked}, 'errors': []}
        except Exception as e:
            return {'success': False, 'message': 'Error ranking candidates', 'data': None, 'errors': [str(e)]}

    def analyze_match(self, resume_text, job_description):
        try:
            if not resume_text or not job_description:
                return {
                    'success': False,
                    'message': 'Resume and job description are required',
                    'data': None,
                    'errors': ['Missing required input']
                }

            analysis = self.matcher.get_match_analysis(resume_text, job_description)

            # Try to save to database (optional - won't fail if DB is unavailable)
            try:
                if self.db_manager.connect():
                    resume_id = self.db_manager.save_resume(resume_text)
                    job_id = self.db_manager.save_job_description('Analyzed Job', 'Company', job_description)

                    if resume_id and job_id:
                        match_details = {
                            'matching_skills': analysis.get('matching_skills', []),
                            'missing_skills': analysis.get('missing_skills', []),
                            'resume_skills': analysis.get('resume_skills', []),
                            'jd_skills': analysis.get('jd_skills', [])
                        }
                        self.db_manager.save_resume_match(
                            resume_id,
                            job_id,
                            analysis.get('match_score', 0),
                            analysis.get('skill_match_percentage', 0),
                            match_details
                        )

                        for skill in analysis.get('resume_skills', []):
                            skill_id = self.db_manager.save_skill(skill, 'technical')
                            if skill_id:
                                self.db_manager.link_resume_skill(resume_id, skill_id)

                        for skill in analysis.get('jd_skills', []):
                            skill_id = self.db_manager.save_skill(skill, 'technical')
                            if skill_id:
                                is_required = skill in analysis.get('missing_skills', [])
                                self.db_manager.link_job_skill(job_id, skill_id, is_required)

                    self.db_manager.disconnect()
            except Exception as db_error:
                print(f"⚠ Database save failed (continuing without DB): {db_error}")

            return {
                'success': True,
                'message': 'Match analysis completed successfully',
                'data': analysis,
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error analyzing match',
                'data': None,
                'errors': [str(e)]
            }

    def get_sample_data(self):
        """Get list of resumes and job descriptions from database instead of sample data"""
        try:
            resumes = self.get_resumes_from_db()
            job_descriptions = self.get_job_descriptions_from_db()
            
            # Format resume list for dropdown
            resume_list = []
            for resume in resumes:
                resume_list.append({
                    'id': resume['resume_id'],
                    'name': f"{resume['resume_title']} - {resume['candidate_name']}"
                })
            
            # Format job description list for dropdown
            job_list = []
            for job in job_descriptions:
                job_list.append({
                    'id': job['job_id'],
                    'name': f"{job['job_title']} - {job['company_name']}"
                })
            
            return {
                'success': True,
                'message': 'Data retrieved successfully from database',
                'data': {
                    'resumes': resume_list,
                    'job_descriptions': job_list
                },
                'errors': []
            }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error retrieving data from database',
                'data': None,
                'errors': [str(e)]
            }

    def get_sample_content(self, sample_type, name):
        """Get resume or job description content from database by ID"""
        try:
            if sample_type == 'resume':
                # Name is actually the resume_id
                try:
                    resume_id = int(name)
                    resume = self.get_resume_by_id(resume_id)
                    
                    if resume:
                        return {
                            'success': True,
                            'message': 'Resume retrieved successfully from database',
                            'data': {'content': resume['resume_text']},
                            'errors': []
                        }
                    else:
                        return {
                            'success': False,
                            'message': 'Resume not found',
                            'data': None,
                            'errors': [f'Resume with ID {resume_id} not found']
                        }
                except ValueError:
                    return {
                        'success': False,
                        'message': 'Invalid resume ID',
                        'data': None,
                        'errors': ['Resume ID must be a number']
                    }
            elif sample_type == 'job_description':
                # Name is actually the job_id
                try:
                    job_id = int(name)
                    job_description = self.get_job_description_by_id(job_id)
                    
                    if job_description:
                        return {
                            'success': True,
                            'message': 'Job description retrieved successfully from database',
                            'data': {'content': job_description['job_description_text']},
                            'errors': []
                        }
                    else:
                        return {
                            'success': False,
                            'message': 'Job description not found',
                            'data': None,
                            'errors': [f'Job description with ID {job_id} not found']
                        }
                except ValueError:
                    return {
                        'success': False,
                        'message': 'Invalid job description ID',
                        'data': None,
                        'errors': ['Job description ID must be a number']
                    }
            else:
                return {
                    'success': False,
                    'message': 'Invalid sample type',
                    'data': None,
                    'errors': ['Sample type must be "resume" or "job_description"']
                }
        except Exception as e:
            return {
                'success': False,
                'message': 'Error retrieving content from database',
                'data': None,
                'errors': [str(e)]
            }