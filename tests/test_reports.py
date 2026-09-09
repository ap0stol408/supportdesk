import json

from tests.helpers import ApiCase


class ReportTests(ApiCase):
    def test_csv_report(self) -> None:
        response = self.app.handle("GET", "/api/reports?format=csv", self.alice)
        self.assertEqual(response.status, 200)
        self.assertIn("Generating report in csv", json.loads(response.body)["output"])
