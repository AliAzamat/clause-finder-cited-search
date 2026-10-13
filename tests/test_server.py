import json
import threading
import unittest
import urllib.parse
import urllib.request
from http.server import HTTPServer

from clausefinder.server import find, make_handler
from clausefinder.store import ingest_folder, open_index


class ServerTests(unittest.TestCase):
    def test_find_returns_only_verified_results(self):
        db = open_index()
        ingest_folder(db, "data/contracts")
        results = find(db, "data/contracts", "Where is arbitration held?")
        self.assertTrue(results)
        self.assertTrue(all(r["verified"] for r in results))
        self.assertEqual((results[0]["doc"], results[0]["clause"]), ("nimbus-saas.txt", "6"))

    def test_http_search_endpoint(self):
        db = open_index()
        ingest_folder(db, "data/contracts")
        server = HTTPServer(("127.0.0.1", 0), make_handler(db, "data/contracts"))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        url = f"http://127.0.0.1:{server.server_port}/search?q=" + urllib.parse.quote("What is the notice of non-renewal period?")
        data = json.load(urllib.request.urlopen(url))
        server.shutdown()
        self.assertEqual(data["results"][0]["clause"], "4")


if __name__ == "__main__":
    unittest.main()
