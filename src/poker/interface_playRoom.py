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
        
        #icons joueurs :
        my_player = pg.image.load('icons/player_basic_image.png')
        self.player_icon = my_player.convert_alpha() # Pour gérer la transparence
        self.player_icon = pg.transform.scale(self.player_icon,(100,100))

        my_AI = pg.image.load('icons/player_AI_lv4(Evil_Lime).png')
        self.AI_icon = my_AI.convert_alpha() # Pour gérer la transparence
        self.AI_icon = pg.transform.scale(self.AI_icon,(100,100))

        self.client = client
        
        self.players_xy = [(430, 500),(780, 500),(430, 40),(780, 40),(100, 250),(1080, 250)] # liste des coordonnées de placement des joueurs autour de la table à déterminée

        #boutons :
        self.input_quit = Button(20, 30, 200, 50, text = "Quitter")
        self.bet_1 = Button(900, 500, 100, 50, text = "Se coucher")
        self.bet_2 = Button(1000, 500, 100, 50, text = "Check")
        self.bet_3 = Button(1000, 500, 100, 50, text = "Suivre")
        self.input_mise = InputBox(900, 550, 300, 20,text='Mise',centered=True)

    def mainloop(self):
        clock = pg.time.Clock()
        done = False

        while not done:
            if self.client.me['isPlaying'] :
                if self.client.info['mise'] == 0 :
                    self.bet_1 = Button(900, 500, 100, 50, text = "Se coucher")
                    self.bet_2 = Button(1000, 500, 100, 50, text = "Check")
                    self.bet_3 = Button(1100, 500, 100, 50, text = "Miser")
                    txt_1 = "COUCHER"
                    txt_2 = "CHECK"
                    txt_3 = "MISE"
                elif self.client.me["mise"] == self.client.info["mise"] :
                    self.bet_1 = Button(900, 500, 100, 50, text = "Se coucher")
                    self.bet_2 = Button(1000, 500, 100, 50, text = "Check")
                    self.bet_3 = Button(1100, 500, 100, 50, text = "Relancer")
                    txt_1 = "COUCHER"
                    txt_2 = "CHECK"
                    txt_3 = "RELANCE"
                else :
                    self.bet_1 = Button(900, 500, 100, 50, text = "Se coucher")
                    self.bet_2 = Button(1000, 500, 100, 50, text = "Suivre")
                    self.bet_3 = Button(1100, 500, 100, 50, text = "Relancer")
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
                self.input_mise.handle_event(event)
                
            
            self.playRoom.blit(self.bg,(0,0))

            for button in input_buttons : 
                button.draw(self.playRoom)
             
            self.input_mise.draw(self.playRoom)

            #affichage des cartes :
            cards = self.client.info['board']
            for i in range(len(cards)):
                img_card = pg.image.load('cards/'+cards[i]+'.jpg')
                img_card = pg.transform.scale(img_card,(100,100))
                img_card = img_card.convert_alpha()
                self.playRoom.blit(img_card,(400+100*i,300))
                
           # affichage joueurs :
            font = pg.font.Font('freesansbold.ttf', 15)
            for k, player in enumerate(self.client.info['players']) :
                if k in [0,1] :
                    offset = (-30,20)
                    offset_mise = (0,-50)
                elif k in [2,3] :
                    offset = (-40,50)
                    offset_mise = (0,130)
                elif k == 4 :
                    offset = (50,130)
                    offset_mise = (150,40)
                else : 
                    offset = (50,120)
                    offset_mise = (-100,40)
                    
                if player['isAI'] :
                    self.playRoom.blit(self.AI_icon, self.players_xy[k])
                else :
                    self.playRoom.blit(self.player_icon, self.players_xy[k])

                pos = self.players_xy[k]

                text_pseudo = font.render(player['pseudo'], True, (0, 0, 128))
                textRect_pseudo = text_pseudo.get_rect()
                textRect_pseudo.center = (pos[0] + offset[0], pos[1] + offset[1])
                self.playRoom.blit(text_pseudo, textRect_pseudo)

                text_money = font.render(str(player['money']), True, (0, 0, 128))
                textRect_money = text_money.get_rect()
                textRect_money.center = (pos[0] + offset[0], pos[1] + offset[1]+30)
                self.playRoom.blit(text_money, textRect_money)

                text_mise = font.render(str(player['mise']), True, (0, 0, 128))
                textRect_mise = text_mise.get_rect()
                textRect_mise.center = (pos[0] + offset_mise[0], pos[1] + offset_mise[1])
                self.playRoom.blit(text_mise, textRect_mise)
                    

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
                self.client.action = txt_3 + " " + self.input_mise.text

                self.input_quit.CurrentState = False 

            pg.display.flip()
            clock.tick(30)
        pg.quit()
        return ""

