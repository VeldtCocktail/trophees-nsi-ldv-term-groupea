# Projet : SilvaDaVinci
# Auteurs : Mathéo PASQUIER, Maden USSEREAU, Léon RAIFAUD, Charlélie PINEAU

# importation des bibliothèques nécessaires
import http.server
import socketserver
import time
import socket

def lancer_serveur():
    """
    Entrées \\: \n
        Aucune

    Rôle \\: \n
        Créer un serveur local et le lancer

    Sortie \\: \n
        None
    """
    # on crée un serveur capable de gérer les requêtes HTTP
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", 8000), handler) as httpd:
        print("Serveur ouvert sur http://127.0.0.1:8000")
        httpd.serve_forever()

def attendre_serveur(hote, port = 8000, timeout = 5.0, intervalle = 0.05):
    """
    Entrées \\: \n
        hote:str : adresse du serveur HTTP local
        port:int : port du serveur HTTP local
        timeout:float : durée maximale d'attente en secondes
        intervalle:float : intervalle entre chaque tentative en secondes
    Rôle \\: \n
        Bloquer jusqu'à ce que le serveur HTTP local soit prêt à accepter des
        connexions, ou jusqu'à expiration du délai d'attente
    Sortie \\: \n
        None
    """
    echeance = time.time() + timeout
    # tant que l'échéance n'est pas dépassée
    while time.time() < echeance:
        try:
            # on tente une connexion TCP au serveur
            with socket.create_connection((hote, port), timeout=intervalle):
                return  # le serveur répond : on peut continuer
            
        except OSError:
            # le serveur n'est pas encore prêt : on attend un peu
            time.sleep(intervalle)

    print(
        f"Avertissement : le serveur {hote}:{port} n'a pas répondu après \
        {timeout} s"
    )