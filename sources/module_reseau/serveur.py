import http.server
import socketserver

def lancer_serveur():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", 8000), handler) as httpd:
        httpd.serve_forever()
