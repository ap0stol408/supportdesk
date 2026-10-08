import tempfile
import unittest
from pathlib import Path

from supportdesk.auth import SessionRegistry
from supportdesk.config import Settings
from supportdesk.database import initialize
from supportdesk.web import Application


class ApiCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.settings = Settings(Path(self.temp.name) / "db.sqlite3", Path(self.temp.name) / "files")
        initialize(self.settings.database)
        self.settings.attachments.mkdir()
        self.sessions = SessionRegistry()
        self.alice = {"Authorization": f"Bearer {self.sessions.issue(1)}"}
        self.bob = {"Authorization": f"Bearer {self.sessions.issue(2)}"}
        self.app = Application(self.settings, self.sessions)

