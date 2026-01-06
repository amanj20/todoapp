import os
import sqlite3


def get_db_path():
    return os.getenv("DATABASE_PATH", "todo.sqlite3")


def connect():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        # New installs: created_at has a default
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Migration for older DBs: add created_at without DEFAULT (SQLite limitation on ALTER)
        cols = [r["name"]
                for r in conn.execute("PRAGMA table_info(tasks)").fetchall()]
        if "created_at" not in cols:
            conn.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT")
            conn.execute(
                "UPDATE tasks SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")

        conn.commit()
