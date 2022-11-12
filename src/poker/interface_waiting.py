import pygame as pg
from pygame.locals import *

from interface_elements import *


class GUI_waiting:
    def __init__(self):
        pg.init()
        #create the window :
        self.waiting = pg.display.set_mode([960, 720])
        pg.display.set_caption("Salle d'attente")
        
        #background : 
        my_bg=pg.image.load('backgrounds/poker_background.jpg')
        self.bg = pg.transform.scale(my_bg, (960, 720))

        
    def mainloop(self):
        clock = pg.time.Clock()
        input_button1 = Button(20, 30, 200, 50, (255, 250, 250),
                     (255, 0, 0), "TimesNewRoman",
                     (255, 255, 255), "Quitter la salle")

        input_button2 = Button(500, 500, 200, 50, (255, 250, 250),
                     (255, 0, 0), "TimesNewRoman",
                     (255, 255, 255), "Lancer la partie !")

        input_buttons = [input_button1,input_button2]
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                for button in input_buttons :
                    # CHECK THE POSITION OF THE MOUSE
                    mouse_pos = pg.mouse.get_pos()
                    # CHECKING THE MOUSE CLICK EVENT
                    mouse_click = pg.mouse.get_pressed()
                    button.handle_event(event)

            self.waiting.blit(self.bg,(0,0))
            for button in input_buttons : 
                button.draw(self.waiting)

            if input_button1.CurrentState:
                input_button1.CurrentState = False
                pg.quit()
                return "HOME"

            if input_button2.CurrentState:
                input_button2.CurrentState = False
                pg.quit()
                return "PLAY"

            pg.display.flip()
            clock.tick(30)
        pg.quit()
        return ""