from interface_waiting import GUI_waiting
from interface_home import GUI_homepage
from interface_playRoom import GUI_playRoom
from interface_client import Client_interface as Client

if __name__ == "__main__":
    done = False
    screen = "HOME"
    connected = False # Placeholder pour limiter la création de multiples clients en alternant HOME et WAITING.

    while not done:
        if screen == "HOME":
            gui = GUI_homepage()
            screen, pseudo = gui.mainloop()
            if not connected and screen == "WAITING" : 
                # L'ajout de "screen == WAITING" protège d'une fermeture de la fenêtre qui provoquerait une connexion non désirée
                client = Client(pseudo) 
                # Création à la fin de gui.mainloop(), i.e. lorsque l'écran HOME est quitté
                connected = True
        elif screen == "WAITING":
            print(f"Bienvenue, {str(pseudo)}")
            gui = GUI_waiting(client)
            screen = gui.mainloop()
            if screen == "HOME" : 
                # Déconnexion de la salle d'attente lorsqu'on la quitte
                client.quit() 
                connected = False  
        elif screen == "PLAY":
            gui = GUI_playRoom(client)
            screen = gui.mainloop()
            if screen == "HOME" :
                client.quit()
                connected = False
        elif screen == "":
            client.quit()
            done = True