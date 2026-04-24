from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open("s1.log", "a", encoding="utf-8") as f:
            f.write("S1 received request\n")

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Response from S1")

server = HTTPServer(("127.0.0.1", 8001), Handler)
print("S1 running at port 8001")
server.serve_forever()