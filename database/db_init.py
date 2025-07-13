import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "inventory.db"
schema_path = r"C:\Users\glori\OneDrive\Documents\GitHub\trial-for-dsa-assignment\data base\schema.sql"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get the absolute path to schema.sql
    schema_path = Path(__file__).parent / "schema.sql"  # 👈 Magic fix!

    with open(schema_path, "r") as f:  # Now it’ll always find the file
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH}")


if __name__ == "__main__":
    init_db()