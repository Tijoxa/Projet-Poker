import pygame as pg
from pygame.locals import *

from interface_elements import *

class GUI_playRoom:
    def __init__(self, client):
        pg.init()
        #create the window :
        self.playRoom = pg.display.set_mode([1280, 650])
        pg.display.set_caption("Centrale Poker ")
        
        #background : image temporaire 
        my_bg = pg.image.load('backgrounds/table_gimp_image.png')
        self.bg = pg.transform.scale(my_bg, (1280, 650))
        
        
        self.client = client
        self.players_xy = [] # TODO : liste des coordonnées de placement des joueurs autour de la table à déterminée
        #boutons :
        self.input_quit = Button(20, 30, 200, 50, text = "Quitter")
        


        
    def mainloop(self):
        clock = pg.time.Clock()
        input_buttons = [self.input_quit]
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

            self.playRoom.blit(self.bg,(0,0))
            for button in input_buttons : 
                button.draw(self.playRoom)
             
            #affichage des cartes :
            cards = self.client.info['board']
            for i in range(len(cards)):
                img_card = pg.image.load('cards/'+cards[i]+'.jpg')
                self.playRoom.blit(img_card,(400+50*i,300)) #TODO : valeurs à déterminer précisément
                
           #affichage joueurs :
               #TODO : ...

            if self.input_quit.CurrentState:
                self.input_quit.CurrentState = False
                pg.quit()
                return "HOME"

            pg.display.flip()
            clock.tick(30)
        pg.quit()
        return ""

