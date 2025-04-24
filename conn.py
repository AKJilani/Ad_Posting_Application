import sqlite3

def get_connection():
    conn = sqlite3.connect('db/flat.db')
    conn.row_factory = sqlite3.Row  # For dictionary-style access
    return conn
