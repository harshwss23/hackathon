#!/usr/bin/env python3
"""
StoryLens AI 2.0 - Unified Application Launcher
Launches local web server for StoryLens AI 2.0 6-view UI workspace.
"""

import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from storylens.backend.main import handle_investigate, handle_simulate
from storylens.evaluation.evaluate import run_evaluation_benchmark

PORT = 8080
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "storylens", "frontend"))

class StoryLensHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/api/investigate":
            scenario = query.get("scenario", ["supply_chain"])[0]
            persona = query.get("persona", ["executive"])[0]
            res = handle_investigate(scenario, persona)
            self._send_json(res)
            return

        if path == "/api/evaluate":
            res = run_evaluation_benchmark()
            self._send_json(res)
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/simulate":
            content_len = int(self.headers.get('Content-Length', 0))
            post_body = self.rfile.read(content_len)
            data = json.loads(post_body) if post_body else {}
            pct = data.get("reallocate_pct", 30.0)
            res = handle_simulate(pct)
            self._send_json(res)
            return

        self.send_error(404, "Endpoint Not Found")

    def _send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

def main():
    print(f"=========================================================")
    print(f"  STORYLENS AI 2.0 - ENTERPRISE DECISION INTELLIGENCE   ")
    print(f"  Accenture Innovation Challenge 2026 - Track 3         ")
    print(f"=========================================================")
    print(f" Launching Server at: http://localhost:{PORT}")
    print(f" Frontend Workspace: {FRONTEND_DIR}")
    print(f"=========================================================")

    server = HTTPServer(("0.0.0.0", PORT), StoryLensHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    main()
