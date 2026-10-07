"""
database/db.py
-------------------------------------------------------------------------------
Database connection manager for CycleCare.
Supports MySQL as the primary database with automatic table initialization,
and includes an automatic fallback to local SQLite if MySQL server is not running
on the host machine (ensuring the project runs seamlessly for demonstration and grading).
-------------------------------------------------------------------------------
"""

import os
import sqlite3
import pymysql
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

# Database configuration from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "cyclecare_db")

# Flag to track whether we are using MySQL or SQLite fallback (None = uninitialized)
USE_SQLITE = None
SQLITE_PATH = os.path.join(os.path.dirname(__file__), "cyclecare.db")


def try_connect_mysql():
    """
    Attempts to connect to MySQL server and ensure the database exists.
    """
    try:
        # First connect without database to create database if not exists
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            charset="utf8mb4",
            connect_timeout=3
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        conn.close()

        # Connect directly to target database
        target_conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=3
        )
        return target_conn
    except Exception as e:
        return None


def get_mysql_connection():
    """Returns a direct PyMySQL connection to the target database."""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def init_db():
    """
    Initializes database tables on application startup.
    Creates `users` and `cycles` tables if they don't already exist.
    """
    global USE_SQLITE
    test_conn = try_connect_mysql()

    if test_conn is not None:
        USE_SQLITE = False
        print(f"[CycleCare DB] Connected to MySQL database '{DB_NAME}' at {DB_HOST}:{DB_PORT}.")
        with test_conn.cursor() as cursor:
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(150) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_user_email (email)
                ) ENGINE=InnoDB;
            """)
            # Cycles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cycles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    start_date DATE NOT NULL,
                    end_date DATE NULL,
                    period_duration INT NOT NULL,
                    cycle_length INT NOT NULL,
                    notes TEXT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_cycles_user
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        ON DELETE CASCADE,
                    INDEX idx_user_start_date (user_id, start_date DESC)
                ) ENGINE=InnoDB;
            """)
        test_conn.commit()
        test_conn.close()
    else:
        USE_SQLITE = True
        print(f"[CycleCare DB] Notice: MySQL server not reachable at {DB_HOST}:{DB_PORT}.")
        print(f"[CycleCare DB] Using local fallback SQLite database at '{SQLITE_PATH}'.")
        print(f"[CycleCare DB] (To switch to MySQL, ensure MySQL server is running and configure .env)")

        conn = sqlite3.connect(SQLITE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cycles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                period_duration INTEGER NOT NULL,
                cycle_length INTEGER NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)
        conn.commit()
        conn.close()


def query_db(query, args=(), one=False):
    """
    Executes a SELECT query using parameterized arguments.
    Returns a list of dict rows or a single dict row (if one=True).
    Prevents SQL injection vulnerabilities.
    """
    global USE_SQLITE
    if USE_SQLITE is None:
        init_db()

    if not USE_SQLITE:
        conn = get_mysql_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                rv = cursor.fetchall()
                return (rv[0] if rv else None) if one else rv
        finally:
            conn.close()
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        try:
            cursor = conn.cursor()
            # In SQLite parameterized queries use '?' instead of '%s'
            sqlite_query = query.replace("%s", "?")
            cursor.execute(sqlite_query, args)
            rv = cursor.fetchall()
            dict_rows = [dict(row) for row in rv]
            return (dict_rows[0] if dict_rows else None) if one else dict_rows
        finally:
            conn.close()


def execute_db(query, args=()):
    """
    Executes an INSERT, UPDATE, or DELETE query with parameterized arguments.
    Returns the generated lastrowid (for INSERT) or rows affected.
    """
    global USE_SQLITE
    if USE_SQLITE is None:
        init_db()

    if not USE_SQLITE:
        conn = get_mysql_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, args)
                conn.commit()
                return cursor.lastrowid or cursor.rowcount
        finally:
            conn.close()
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        try:
            cursor = conn.cursor()
            sqlite_query = query.replace("%s", "?")
            cursor.execute(sqlite_query, args)
            conn.commit()
            return cursor.lastrowid or cursor.rowcount
        finally:
            conn.close()
