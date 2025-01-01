import sqlite3
import os
from pathlib import Path

def get_imessage_schema():
    """Read and return the schema of the iMessage database."""
    db_path = os.path.expanduser("~/Library/Messages/chat.db")
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"iMessage database not found at {db_path}")
    
    # Create a copy of the database to avoid locking the original
    temp_db = "/tmp/chat_temp.db"
    os.system(f"cp '{db_path}' '{temp_db}'")
    
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            schema[table_name] = columns
            
        return schema
    finally:
        conn.close()
        os.remove(temp_db)

if __name__ == "__main__":
    schema = get_imessage_schema()
    for table, columns in schema.items():
        print(f"\nTable: {table}")
        for col in columns:
            print(f"  {col}")