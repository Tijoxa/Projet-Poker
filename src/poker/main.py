from interface_waiting import GUI_waiting
from interface_home import GUI_homepage
from interface_playRoom import GUI_playRoom
import ctypes

#pour afficher les fenètres en HD 1080x1920 (1.5x plus grand que le 720p)
#ctypes.windll.shcore.SetProcessDpiAwareness(1)

if __name__ == "__main__":
    gui = GUI_homepage()
    screen = gui.mainloop()
    done = False

    while not done:
        if screen == "WAITING":
            gui = GUI_waiting()
            screen = gui.mainloop()
        elif screen == "HOME":
            gui = GUI_homepage()
            screen = gui.mainloop()
        elif screen == "PLAY":
            gui = GUI_playRoom()
            screen = gui.mainloop()
        elif screen == "":
            done = True