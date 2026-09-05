from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
import sqlite3


@contextmanager
def connect(path: Path) -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY,
                owner_id INTEGER NOT NULL REFERENCES users(id),
                title TEXT NOT NULL CHECK(length(title) BETWEEN 1 AND 200),
                body TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS issues_owner_created
                ON issues(owner_id, created_at);
            """
        )
        db.executemany(
            "INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)",
            [(1, "Alice Demo"), (2, "Bob Demo")],
        )
        db.executemany(
            "INSERT OR IGNORE INTO issues (id, owner_id, title, body) VALUES (?, ?, ?, ?)",
            [
                (1, 1, "Printer offline", "Synthetic Alice ticket"),
                (2, 2, "Account export", "Synthetic Bob private ticket"),
            ],
        )
