import http.server
import socketserver


def lancer_serveur():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", 8000), handler) as httpd:
        print("Serveur ouvert")
        httpd.serve_forever()
        
def fermer_seveur():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("127.0.0.1", 8000), handler) as httpd:
        print("Serveur fermé")
        httpd.shutdown()