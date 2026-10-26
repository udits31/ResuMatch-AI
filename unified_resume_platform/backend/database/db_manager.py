from psycopg2.extras import Json
from unified_resume_platform.backend.database.db_config import get_db_connection, close_db_connection

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.db_enabled = True

    def connect(self):
        try:
            self.connection = get_db_connection()
            if self.connection is None:
                self.db_enabled = False
                return False
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            self.db_enabled = False
            return False

    def disconnect(self):
        try:
            close_db_connection(self.connection)
            self.connection = None
        except Exception as e:
            print(f"Error disconnecting: {e}")

    def save_resume(self, resume_text, candidate_name=None, candidate_email=None):
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            # PostgreSQL returns the new id via RETURNING (there is no lastrowid)
            query = """INSERT INTO resumes (resume_title, resume_text, candidate_name, candidate_email)
                       VALUES (%s, %s, %s, %s) RETURNING resume_id"""
            cursor.execute(query, ('Analyzed Resume', resume_text, candidate_name or 'Candidate', candidate_email))
            resume_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            return resume_id
        except Exception as e:
            print(f"Error saving resume: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def save_job_description(self, job_title, company_name, job_description_text, posted_by=None):
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            query = """INSERT INTO job_descriptions (job_title, company_name, job_description_text, posted_by)
                       VALUES (%s, %s, %s, %s) RETURNING job_id"""
            cursor.execute(query, (job_title, company_name, job_description_text, posted_by))
            job_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            return job_id
        except Exception as e:
            print(f"Error saving job description: {e}")
            if self.connection:
                self.connection.rollback()
            return None

    def save_resume_match(self, resume_id, job_id, match_score, skill_match_percentage, match_details):
        try:
            if not self.connection:
                self.connect()
            cursor = self.connection.cursor()
            # PostgreSQL upsert: ON CONFLICT ... DO UPDATE with EXCLUDED (not VALUES()).
            # JSONB values are passed through psycopg2's Json adapter.
            query = """INSERT INTO resume_matches (resume_id, job_id, match_score, skill_match_percentage,
                      matching_skills, missing_skills, resume_skills, job_skills)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                      ON CONFLICT (resume_id, job_id) DO UPDATE SET
                          match_score = EXCLUDED.match_score,
                          skill_match_percentage = EXCLUDED.skill_match_percentage,
                          matching_skills = EXCLUDED.matching_skills,
                          missing_skills = EXCLUDED.missing_skills,
                          resume_skills = EXCLUDED.resume_skills,
                          job_skills = EXCLUDED.job_skills"""
            cursor.execute(query, (
                resume_id, job_id, match_score, skill_match_percentage,
                Json(match_details.get('matching_skills', [])),
                Json(match_details.get('missing_skills', [])),
                Json(match_details.get('resume_skills', [])),
                Json(match_details.get('jd_skills', []))
            ))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error saving resume match: {e}")
            if self.connection:
                self.connection.rollback()
            return False
