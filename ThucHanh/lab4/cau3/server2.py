from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open("s2.log", "a", encoding="utf-8") as f:
            f.write("S2 received request\n")

        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Response from S2")

server = HTTPServer(("127.0.0.1", 8002), Handler)
print("S2 running at port 8002")
server.serve_forever()


#ab -n 100 -c 10 http://127.0.0.1:8080/
#wrk -t2 -c10 -d10s http://127.0.0.1:8080/