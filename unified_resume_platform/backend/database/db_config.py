import mysql.connector
from mysql.connector import Error
import os

# Database Configuration
# IMPORTANT: Update the password below with your MySQL root password
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',  # ← Updated with actual MySQL password
    'database': 'unified_resume_portal',
    'autocommit': False
}

def get_db_connection():
    """
    Establishes connection to MySQL database
    Returns connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"\n{'='*60}")
        print("DATABASE CONNECTION ERROR")
        print(f"{'='*60}")
        print(f"Error: {e}")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database 'unified_resume_portal' exists")
        print("3. Password in db_config.py is correct")
        print("4. Run: python init_database.py (to setup database)")
        print(f"{'='*60}\n")
        return None

def close_db_connection(connection):
    """Safely closes database connection"""
    if connection and connection.is_connected():
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
