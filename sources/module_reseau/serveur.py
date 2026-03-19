import http.server
import socketserver

def lancer_serveur():
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", 8000), handler) as httpd:
        print("Serveur ouvert sur http://127.0.0.1:8000")
        httpd.serve_forever()