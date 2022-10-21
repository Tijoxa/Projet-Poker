import socket
import threading

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host, port = ('', 5566) # l'adresse est vide car ce sont les clients qui se connectent au serveur et non l'inverse

socket.bind((host, port)) #associe au socket une adresse:: bind((adresse, port))

# server started

while True:
    socket.listen() # ecoute pour les connections
    conn, addr = socket.accept() #le client connecté et son adresse
    print("client connecté!")
    data = ""
    while data != "quit()":
        data = conn.recv(1024)
        data = data.decode("utf8")
        print(data)
        if data!= "quit()":
            awnser = "message reçu!"
            awnser = awnser.encode("utf8")
            conn.sendall(awnser)
    conn.close()
socket.close()
    