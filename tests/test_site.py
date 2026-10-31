import functools
import http.server
from pathlib import Path
import threading
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[1] / "docs"

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT))
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join()

    def test_root_serves_the_application(self):
        self.assertTrue((ROOT / "index.html").is_file(), "The deployment root must have index.html")
        with urllib.request.urlopen(self.url + "/", timeout=5) as response:
            self.assertEqual(response.status, 200)
            html = response.read().decode()
        self.assertIn('id="check-status"', html)
        self.assertIn('id="status"', html)
        self.assertIn('src="app.js"', html)

    def test_application_asset_is_served(self):
        with urllib.request.urlopen(self.url + "/app.js", timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertGreater(len(response.read()), 0)

if __name__ == "__main__":
    unittest.main()
