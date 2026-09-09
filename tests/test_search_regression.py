import json
from urllib.parse import urlencode

from tests.helpers import ApiCase


class SearchRegressionTests(ApiCase):
    def test_sql_fragment_is_literal_search_text(self) -> None:
        query = urlencode({"q": "' OR 1=1 -- "})
        response = self.app.handle("GET", f"/api/issues?{query}", self.alice)
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(response.body)["issues"], [])
