import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv

# Load variables from a local .env file (if present)
load_dotenv()

# Database Configuration — Supabase (PostgreSQL)
# The connection string lives in .env as SUPABASE_DB_URL. Find it in the
# Supabase dashboard: Settings → Database → Connection string → URI.
DATABASE_URL = os.getenv("SUPABASE_DB_URL")

def get_db_connection():
    """
    Establishes connection to the Supabase PostgreSQL database.
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
        connection = psycopg2.connect(DATABASE_URL)
        return connection
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
    """Safely closes database connection"""
    if connection and not connection.closed:
        connection.close()

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
