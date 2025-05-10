import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "noxheaven.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Create tables
        cursor.executescript('''
            -- Enable foreign keys and strict typing
            PRAGMA foreign_keys = ON;
            PRAGMA strict = ON;

            -- Core Save Files
            CREATE TABLE IF NOT EXISTS saves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                game_state TEXT NOT NULL CHECK(json_valid(game_state))  -- JSON
            );

            -- Event History Tracking
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                save_id INTEGER NOT NULL,
                event_type TEXT NOT NULL CHECK(event_type IN ('DIALOGUE', 'LOCATION', 'RELATIONSHIP', 'INVENTORY')),
                event_data TEXT NOT NULL CHECK(json_valid(event_data)),  -- JSON
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(save_id) REFERENCES saves(id) ON DELETE CASCADE
            );

            -- Context Summaries for LLM
            CREATE TABLE IF NOT EXISTS context_summaries (
                save_id INTEGER PRIMARY KEY,
                summary TEXT NOT NULL,
                vector_embedding BLOB,  -- For future semantic search
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(save_id) REFERENCES saves(id) ON DELETE CASCADE
            );

            -- Indexes for Performance
            CREATE INDEX idx_history_save ON history(save_id);
            CREATE INDEX idx_history_type ON history(event_type);
        ''')  # Use full schema from above

        conn.commit()

class DatabaseManager:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.row_factory = sqlite3.Row  # Dict-like access
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized at:", DB_PATH)