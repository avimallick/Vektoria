# metadata_store.py
import sqlite3
from typing import Optional, List, Dict

class MetadataStore:
    def __init__(self, db_path: str = "metadata.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def create_tables(conn):
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS anti_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            problem TEXT,
            category TEXT,
            language TEXT,
            severity TEXT,
            remediation TEXT,
            limitation TEXT,
            examples_json TEXT,
            vector_id INTEGER UNIQUE
        );
        """)
        conn.commit()


    def add(self, id: int, text: str, tags: Optional[str] = None):
        with self.conn:
            self.conn.execute(
                "INSERT INTO metadata (id, text, tags) VALUES (?, ?, ?)",
                (id, text, tags)
            )

    def get(self, id: int) -> Optional[Dict]:
        cursor = self.conn.execute("SELECT * FROM metadata WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "text": row[1], "tags": row[2], "created_at": row[3]}
        return None

    def get_bulk(self, ids: List[int]) -> List[Dict]:
        cursor = self.conn.execute(
            f"SELECT * FROM metadata WHERE id IN ({','.join('?'*len(ids))})", ids
        )
        rows = cursor.fetchall()
        return [
            {"id": row[0], "text": row[1], "tags": row[2], "created_at": row[3]}
            for row in rows
        ]
    
    def get_all(self) -> List[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM anti_patterns")
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "problem": row[3],
                "category": row[4],
                "language": row[5],
                "severity": row[6],
                "remediation": row[7],
                "limitation": row[8],
                "examples": json.loads(row[9]),
                "vector_id": row[10],
            }
            for row in rows
        ]
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM anti_patterns WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "problem": row[3],
                "category": row[4],
                "language": row[5],
                "severity": row[6],
                "remediation": row[7],
                "limitation": row[8],
                "examples": json.loads(row[9]),
                "vector_id": row[10],
            }
        return None



    def close(self):
        self.conn.close()
