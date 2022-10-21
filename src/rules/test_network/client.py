import socket

host, port = ('x.x.x.X', 5566) # cette ip doit être l'ip publique de l'ordinateur sur lequel tourne le serveur, le port doit être en accord avec celui du serveur

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.connect((host, port)) # connexion au serveur
    print("Connexion réussie")
    data = ""
    while data != "/quit": # /quit permet d'arrêter d'utiliser
        data = input("\t>") # message manuel
        data_encoded = data.encode("utf8")
        socket.sendall(data_encoded)
        awnser = socket.recv(1024) # reception et affichage de la réponse
        awnser = awnser.decode("utf8")
        print(awnser)
except ConnectionRefusedError:
    print("Le serveur n'est pas démarré")
except:
    print("Connexion échouée")
finally:
    socket.close()
