"""
db.py  -  Tiny database helper for the Pharmacy Management System.

Wraps the standard-library sqlite3 module so the GUI code stays clean.
Every connection turns foreign-key enforcement ON and returns rows that
can be accessed by column name.
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pharmacy.db")


def get_connection():
    """Open a connection to the pharmacy database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # access columns by name
    conn.execute("PRAGMA foreign_keys = ON;")  # enforce foreign keys
    return conn


def fetch_all(query, params=()):
    """Run a SELECT and return all rows."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchall()
    finally:
        conn.close()


def fetch_one(query, params=()):
    """Run a SELECT and return a single row (or None)."""
    conn = get_connection()
    try:
        return conn.execute(query, params).fetchone()
    finally:
        conn.close()


def execute(query, params=()):
    """Run an INSERT / UPDATE / DELETE and commit. Returns last row id."""
    conn = get_connection()
    try:
        cur = conn.execute(query, params)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()
