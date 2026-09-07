import json
import os
from unittest.mock import patch

from tests.helpers import ApiCase


class DiagnosticsTests(ApiCase):
    def test_environment_snapshot(self) -> None:
        with patch.dict(os.environ, {"LAB_MARKER": "synthetic"}, clear=True):
            response = self.app.handle("GET", "/api/debug", self.alice)
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(response.body)["environment"], {"LAB_MARKER": "synthetic"})
