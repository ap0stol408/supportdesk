import json
from tests.helpers import ApiCase


class ApiTests(ApiCase):
    def test_health_is_public(self) -> None:
        response = self.app.handle("GET", "/health", {})
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(response.body), {"status": "ok"})

    def test_anonymous_cannot_read_queue(self) -> None:
        self.assertEqual(self.app.handle("GET", "/api/issues", {}).status, 401)

    def test_invalid_session_is_rejected(self) -> None:
        self.assertEqual(
            self.app.handle("GET", "/api/issues", {"Authorization": "Bearer invalid"}).status,
            401,
        )

    def test_each_queue_contains_its_own_ticket(self) -> None:
        alice = json.loads(self.app.handle("GET", "/api/issues", self.alice).body)
        bob = json.loads(self.app.handle("GET", "/api/issues", self.bob).body)
        self.assertEqual([item["id"] for item in alice["issues"]], [1])
        self.assertEqual([item["id"] for item in bob["issues"]], [2])

    def test_search(self) -> None:
        response = self.app.handle("GET", "/api/issues?q=Printer", self.alice)
        self.assertEqual(len(json.loads(response.body)["issues"]), 1)

    def test_create_and_read(self) -> None:
        response = self.app.handle(
            "POST", "/api/issues", self.alice,
            json.dumps({"title": "New laptop", "body": "Synthetic request"}).encode(),
        )
        self.assertEqual(response.status, 201)
        issue_id = json.loads(response.body)["id"]
        ticket = json.loads(self.app.handle("GET", f"/api/issues/{issue_id}", self.alice).body)
        self.assertEqual(ticket["title"], "New laptop")
        self.assertEqual(ticket["owner_id"], 1)

    def test_create_ignores_client_owner(self) -> None:
        response = self.app.handle(
            "POST", "/api/issues", self.alice,
            b'{"title":"Owner test","body":"demo","owner_id":2}',
        )
        issue_id = json.loads(response.body)["id"]
        issue = json.loads(self.app.handle("GET", f"/api/issues/{issue_id}", self.alice).body)
        self.assertEqual(issue["owner_id"], 1)

    def test_invalid_bodies(self) -> None:
        for body in (b"broken", b"[]", b'{"title":" "}', b'{"title":42}'):
            with self.subTest(body=body):
                self.assertEqual(self.app.handle("POST", "/api/issues", self.alice, body).status, 400)

    def test_missing_ticket(self) -> None:
        self.assertEqual(self.app.handle("GET", "/api/issues/999", self.alice).status, 404)

    def test_html_detail(self) -> None:
        response = self.app.handle("GET", "/issues/1", self.alice)
        self.assertEqual(response.status, 200)
        self.assertIn(b"Printer offline", response.body)


if __name__ == "__main__":
    unittest.main()
