from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        msg = "Hello from Jenkins CI/CD on Azure!"
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(msg.encode())

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8080), Handler)
    print("Server listening on port 8080...")
    server.serve_forever()