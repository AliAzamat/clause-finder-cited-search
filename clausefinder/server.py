import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from .answer import make_answer
from .check import verify
from .search import search
from .store import ingest_folder, open_index


def find(db, folder, question, k=3):
    results = []
    for hit in search(db, question, k):
        answer = make_answer(hit, question)
        if verify(answer, folder):
            results.append({**answer, "verified": True})
    return results


def make_handler(db, folder):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            url = urlparse(self.path)
            if url.path != "/search":
                self.send_error(404)
                return
            question = parse_qs(url.query).get("q", [""])[0]
            body = json.dumps({"question": question, "results": find(db, folder, question)}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    return Handler


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "data/contracts"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8765
    db = open_index()
    print("indexed", ingest_folder(db, folder), "clauses")
    HTTPServer(("127.0.0.1", port), make_handler(db, folder)).serve_forever()
