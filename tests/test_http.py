from http.client import HTTPConnection
from threading import Thread

from supportdesk.server import make_server
from tests.helpers import ApiCase


class HttpTests(ApiCase):
    def test_http_create_search_read_and_auth(self) -> None:
        with make_server(self.app, 0) as server:
            thread = Thread(target=server.serve_forever, daemon=True)
            thread.start()
            client = HTTPConnection("127.0.0.1", server.server_port, timeout=5)
            try:
                client.request("GET", "/health")
                response = client.getresponse()
                self.assertEqual(response.status, 200)
                response.read()
                client.request("GET", "/api/issues")
                response = client.getresponse()
                self.assertEqual(response.status, 401)
                response.read()
                client.request("POST", "/api/issues", '{"title":"HTTP ticket"}', self.alice)
                response = client.getresponse()
                self.assertEqual(response.status, 201)
                response.read()
                client.request("GET", "/api/issues?q=HTTP", headers=self.alice)
                response = client.getresponse()
                self.assertEqual(response.status, 200)
                self.assertIn(b"HTTP ticket", response.read())
                client.request("GET", "/issues/1", headers=self.alice)
                response = client.getresponse()
                self.assertEqual(response.status, 200)
                self.assertIn(b"Printer offline", response.read())
                client.request(
                    "POST", "/api/issues", headers={**self.alice, "Content-Length": "20000"}
                )
                response = client.getresponse()
                self.assertEqual(response.status, 413)
                response.read()
            finally:
                client.close()
                server.shutdown()
                thread.join(timeout=5)
