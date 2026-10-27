import json
from psycopg2.extras import RealDictCursor, Json
from unified_resume_platform.backend.database.db_config import get_db_connection, close_db_connection


class ProfileRepository:
    """Stores job-seeker profiles in Supabase as JSONB, keyed by a unique name.
    Supports multiple named profiles (list / load / save / delete)."""

    def list_names(self):
        conn = get_db_connection()
        if not conn:
            return []
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT profile_name FROM profiles ORDER BY updated_at DESC")
            rows = cursor.fetchall()
            cursor.close()
            return [r['profile_name'] for r in rows]
        except Exception as e:
            print(f"Error listing profiles: {e}")
            return []
        finally:
            close_db_connection(conn)

    def load(self, name=None):
        """Load a profile by name, or the most recently updated one if name is None.
        Returns the profile dict (with 'profile_name' injected) or None."""
        conn = get_db_connection()
        if not conn:
            return None
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            if name:
                cursor.execute("SELECT profile_name, data FROM profiles WHERE profile_name = %s", (name,))
            else:
                cursor.execute("SELECT profile_name, data FROM profiles ORDER BY updated_at DESC LIMIT 1")
            row = cursor.fetchone()
            cursor.close()
            if not row:
                return None
            data = row['data']
            if isinstance(data, str):
                data = json.loads(data)
            data['profile_name'] = row['profile_name']
            return data
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
        finally:
            close_db_connection(conn)

    def save(self, name, data):
        """Create or update (upsert) a named profile."""
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO profiles (profile_name, data) VALUES (%s, %s)
                   ON CONFLICT (profile_name) DO UPDATE SET data = EXCLUDED.data""",
                (name, Json(data))
            )
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            try:
                conn.rollback()
            except Exception:
                pass
            return False
        finally:
            close_db_connection(conn)

    def delete(self, name):
        conn = get_db_connection()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles WHERE profile_name = %s", (name,))
            conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error deleting profile: {e}")
            try:
                conn.rollback()
            except Exception:
                pass
            return False
        finally:
            close_db_connection(conn)
