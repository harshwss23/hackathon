#!/usr/bin/env python3
"""
StoryLens AI 2.0 - Unified Application Launcher
Launches local web server for StoryLens AI 2.0 6-view UI workspace.
"""

import os
import sys
import json
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

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

        if path == "/api/health":
            self._send_json({
                "status": "healthy",
                "service": "storylens-ai",
                "version": "2.1",
            })
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        try:
            data = self._read_json_body()
            if parsed.path == "/api/simulate":
                pct = data.get("reallocate_pct", 30.0)
                self._send_json(handle_simulate(pct))
                return

        except ValueError as exc:
            self._send_json({"error": str(exc)}, status=400)
            return
        except Exception as exc:
            self._send_json({"error": "Request failed", "detail": str(exc)}, status=500)
            return

        self._send_json({"error": "Endpoint not found"}, status=404)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def _read_json_body(self):
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len > 32768:
            raise ValueError("Request body is too large")
        if content_len == 0:
            return {}
        try:
            return json.loads(self.rfile.read(content_len).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Request body must be valid JSON") from exc

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
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

    server = ThreadingHTTPServer(("0.0.0.0", PORT), StoryLensHTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    main()
