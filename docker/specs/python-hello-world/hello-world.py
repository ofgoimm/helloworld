import random
import string
from http.server import BaseHTTPRequestHandler, HTTPServer

# Generate a random 8-character ID
INSTANCE_ID = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"hello world from {INSTANCE_ID}\n".encode())

# Start HTTP server
HTTPServer(('', 80), HelloHandler).serve_forever()
