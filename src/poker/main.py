from interface_waiting import GUI_waiting
from interface_home import GUI_homepage

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
        elif screen == "":
            done = True