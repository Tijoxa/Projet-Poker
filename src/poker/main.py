from interface_waiting import GUI_waiting
from interface_home import GUI_homepage
from interface_playRoom import GUI_playRoom
from interface_client import Client_interface as Client

if __name__ == "__main__":
    done = False
    screen = "HOME"

    while not done:
        if screen == "HOME":
            gui = GUI_homepage()
            screen, pseudo = gui.mainloop()
            client = Client(pseudo)
            print(screen, pseudo)
        elif screen == "WAITING":
            gui = GUI_waiting(client)
            screen = gui.mainloop()
        elif screen == "PLAY":
            client.send("ready")
            gui = GUI_playRoom(client)
            screen = gui.mainloop()
        elif screen == "":
            done = True