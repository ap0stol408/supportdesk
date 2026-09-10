import json

from tests.helpers import ApiCase


class SecurityRegressionTests(ApiCase):
    def test_another_users_ticket_is_not_returned(self) -> None:
        for route in ("/api/issues/2", "/issues/2"):
            with self.subTest(route=route):
                response = self.app.handle("GET", route, self.alice)
                self.assertEqual(response.status, 404)
                self.assertNotIn(b"Synthetic Bob private ticket", response.body)

    def test_markup_is_rendered_as_text(self) -> None:
        response = self.app.handle(
            "POST", "/api/issues", self.alice,
            json.dumps({"title": "<b>demo</b>", "body": "<script>demo</script>"}).encode(),
        )
        issue_id = json.loads(response.body)["id"]
        detail = self.app.handle("GET", f"/issues/{issue_id}", self.alice)
        self.assertIn(b"&lt;script&gt;demo&lt;/script&gt;", detail.body)
        self.assertNotIn(b"<script>", detail.body)
