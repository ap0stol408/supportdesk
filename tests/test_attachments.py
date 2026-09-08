from tests.helpers import ApiCase


class AttachmentTests(ApiCase):
    def test_download(self) -> None:
        (self.settings.attachments / "receipt.txt").write_text("Synthetic receipt")
        response = self.app.handle("GET", "/api/attachments?name=receipt.txt", self.alice)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body, b"Synthetic receipt")

    def test_missing_attachment(self) -> None:
        response = self.app.handle("GET", "/api/attachments?name=missing.txt", self.alice)
        self.assertEqual(response.status, 404)
