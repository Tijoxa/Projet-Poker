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
        self.bet_1 = Button(700, 500, 100, 50, text = "Se coucher")
        self.bet_2 = Button(800, 500, 100, 50, text = "Check")
        self.bet_3 = Button(900, 500, 100, 50, text = "Suivre")
        self.input_mise = InputBox(900, 550, 100, 50,text='Mise',centered=True)

    def mainloop(self):
        clock = pg.time.Clock()
        done = False

        while not done:
            if self.client.me['isPlaying'] :
                if self.client.info['mise'] == 0 :
                    self.bet_1 = Button(700, 500, 100, 50, text = "Se coucher")
                    self.bet_2 = Button(800, 500, 100, 50, text = "Check")
                    self.bet_3 = Button(900, 500, 100, 50, text = "Miser")
                    txt_1 = "COUCHER"
                    txt_2 = "CHECK"
                    txt_3 = "MISE"
                elif self.client.me["mise"] == self.client.info["mise"] :
                    self.bet_1 = Button(700, 500, 100, 50, text = "Se coucher")
                    self.bet_2 = Button(800, 500, 100, 50, text = "Check")
                    self.bet_3 = Button(900, 500, 100, 50, text = "Relancer")
                    txt_1 = "COUCHER"
                    txt_2 = "CHECK"
                    txt_3 = "RELANCE"
                else :
                    self.bet_1 = Button(700, 500, 100, 50, text = "Se coucher")
                    self.bet_2 = Button(800, 500, 100, 50, text = "Suivre")
                    self.bet_3 = Button(900, 500, 100, 50, text = "Relancer")
                    txt_1 = "COUCHER"
                    txt_2 = "SUIVRE"
                    txt_3 = "RELANCE"

                input_buttons = [self.input_quit,self.bet_1,self.bet_2,self.bet_3]
            else :
                input_buttons = [self.input_quit]

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
             
            self.input_mise.draw(self.playRoom)

            #affichage des cartes :
            cards = self.client.info['board']
            for i in range(len(cards)):
                img_card = pg.image.load('cards/'+cards[i]+'.jpg')
                img_card = pg.transform.scale(img_card,(100,100))
                self.playRoom.blit(img_card,(400+100*i,300)) #TODO : valeurs à déterminer précisément
                
           #affichage joueurs :
               #TODO : ...

            if self.input_quit.CurrentState:
                self.input_quit.CurrentState = False
                pg.quit()
                return "HOME"

            if self.bet_1.CurrentState :
                self.client.action = txt_1
                self.input_quit.CurrentState = False 
            
            if self.bet_2.CurrentState :
                self.client.action = txt_2
                self.input_quit.CurrentState = False 
            
            if self.bet_3.CurrentState :
                self.client.action = txt_3 + self.input_mise.text

                self.input_quit.CurrentState = False 

            pg.display.flip()
            clock.tick(30)
        pg.quit()
        return ""

