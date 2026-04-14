from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from datetime import datetime

DATA_DIR = "webhook-data"


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        os.makedirs(DATA_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(DATA_DIR, f"webhook_{timestamp}.json")

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n[{timestamp}] Webhook received! Saved to {filename}")
        print(json.dumps(data, indent=2))

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode())


if __name__ == "__main__":
    port = 8000
    server = HTTPServer(("0.0.0.0", port), WebhookHandler)
    print(f"Webhook server listening on port {port}...")
    print("Waiting for incoming webhooks...\n")
    server.serve_forever()
