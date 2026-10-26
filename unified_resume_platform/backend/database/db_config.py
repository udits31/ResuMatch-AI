import os
import psycopg2
from psycopg2 import Error, pool
from dotenv import load_dotenv

# Load variables from a local .env file (if present)
load_dotenv()

# Database Configuration — Supabase (PostgreSQL)
# The connection string lives in .env as SUPABASE_DB_URL. Find it in the
# Supabase dashboard: Settings → Database → Connection string → URI.
DATABASE_URL = os.getenv("SUPABASE_DB_URL")

# Reuse a small pool of connections instead of opening a new one (TCP + TLS +
# auth) on every query. This makes dropdown/content loading from the remote
# Supabase database noticeably faster.
_CONNECTION_POOL = None

def _get_pool():
    global _CONNECTION_POOL
    if _CONNECTION_POOL is None and DATABASE_URL:
        _CONNECTION_POOL = pool.ThreadedConnectionPool(1, 5, DATABASE_URL)
    return _CONNECTION_POOL

def get_db_connection():
    """
    Borrow a connection from the pool (the pool is created on first use).
    Returns connection object or None if connection fails.
    """
    if not DATABASE_URL:
        print(f"\n{'='*60}")
        print("DATABASE CONFIG ERROR")
        print(f"{'='*60}")
        print("SUPABASE_DB_URL is not set.")
        print("Copy .env.example to .env and paste your Supabase connection string.")
        print(f"{'='*60}\n")
        return None

    try:
        return _get_pool().getconn()
    except Error as e:
        print(f"\n{'='*60}")
        print("DATABASE CONNECTION ERROR")
        print(f"{'='*60}")
        print(f"Error: {e}")
        print("\nPlease check:")
        print("1. SUPABASE_DB_URL in .env is correct (and password is filled in)")
        print("2. The Supabase project is not paused (free projects pause when idle)")
        print("3. You have run supabase_schema.sql and insert_data.sql in the SQL Editor")
        print(f"{'='*60}\n")
        return None

def close_db_connection(connection):
    """Return the connection to the pool (reset first so no transaction lingers)."""
    pool_ref = _get_pool()
    if not connection or pool_ref is None:
        return
    try:
        if not connection.closed:
            connection.rollback()
    except Exception:
        pass
    try:
        pool_ref.putconn(connection)
    except Exception:
        pass

def test_connection():
    """Test if database connection works"""
    conn = get_db_connection()
    if conn:
        print("✓ Database connection successful")
        close_db_connection(conn)
        return True
    else:
        print("✗ Database connection failed")
        return False
