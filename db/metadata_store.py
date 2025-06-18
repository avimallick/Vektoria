# metadata_store.py
import sqlite3
from typing import Optional, List, Dict

class MetadataStore:
    def __init__(self, db_path: str = "metadata.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS metadata (
                    id INTEGER PRIMARY KEY,
                    text TEXT NOT NULL,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

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

    def close(self):
        self.conn.close()
