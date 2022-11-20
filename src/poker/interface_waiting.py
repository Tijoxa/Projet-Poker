import pygame as pg
from pygame.locals import *

from interface_elements import *

class GUI_waiting:
    def __init__(self, client):
        pg.init()
        #create the window :
        self.waiting = pg.display.set_mode([1023, 510])
        pg.display.set_caption("Salle d'attente")
        
        #background : 
        my_bg = pg.image.load('backgrounds/waiting_background.png')
        self.bg = pg.transform.scale(my_bg, (1023, 510))
        
        #connected players : 
        self.list_players = []
        self.client = client

        
    def mainloop(self):
        clock = pg.time.Clock()
        #buttons :
        button_quit = Button(20, 30, 200, 50, text = "Quitter la salle")
        button_play = Button(800, 30, 200, 50, text = "Lancer la partie !")
        button_add_player = Button(80, 360, 50, 50, shape = 'circle',
                                   colour_mouse_on = 'black', colour_mouse_off = 'green',
                                   textSize = 30, text = "+")
        button_del_player = Button(240, 360, 50, 50, shape = 'circle',
                                   colour_mouse_on = 'black',
                                   textSize = 30, text = "-")
        input_buttons = [button_quit,button_play, 
                         button_add_player, button_del_player]
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
                
            for player in self.list_players:
                pass

            if button_quit.CurrentState:
                button_quit.CurrentState = False
                pg.quit()
                return "HOME"

            if button_play.CurrentState:
                button_play.CurrentState = False
                pg.quit()
                return "PLAY"

            pg.display.flip()
            clock.tick(30)
        pg.quit()
        return ""