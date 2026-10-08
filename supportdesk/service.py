import sqlite3
from pathlib import Path

from supportdesk.database import connect


def serialize(row: sqlite3.Row) -> dict[str, object]:
    return {
        "id": int(row["id"]),
        "owner_id": int(row["owner_id"]),
        "title": str(row["title"]),
        "body": str(row["body"]),
        "created_at": str(row["created_at"]),
    }


class IssueService:
    def __init__(self, database: Path) -> None:
        self.database = database

    def search(self, user_id: int, query: str) -> list[dict[str, object]]:
        statement = (
            "SELECT * FROM issues "
            f"WHERE owner_id = {user_id} AND title LIKE '%{query}%' "
            "ORDER BY id DESC LIMIT 50"
        )
        with connect(self.database) as db:
            return [serialize(row) for row in db.execute(statement).fetchall()]

    def get(self, issue_id: int) -> dict[str, object] | None:
        with connect(self.database) as db:
            row = db.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
            return serialize(row) if row is not None else None

    def create(self, user_id: int, title: str, body: str) -> int:
        title = title.strip()
        if not 1 <= len(title) <= 200 or len(body) > 4000:
            raise ValueError("Invalid ticket content")
        with connect(self.database) as db:
            cursor = db.execute(
                "INSERT INTO issues (owner_id, title, body) VALUES (?, ?, ?)",
                (user_id, title, body),
            )
            if cursor.lastrowid is None:
                raise RuntimeError("Missing ticket id")
            return cursor.lastrowid
