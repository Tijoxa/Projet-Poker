import pygame as pg
from pygame.locals import *

from interface_elements import *

class GUI_playRoom:
    def __init__(self, client):
        pg.init()
        #create the window :
        self.playRoom = pg.display.set_mode([1280, 650])
        pg.display.set_caption("Centrale Poker ")

        self.font = pg.font.Font('freesansbold.ttf', 15)

        #background : image temporaire 
        my_bg = pg.image.load('backgrounds/table_gimp_image.png')
        self.bg = pg.transform.scale(my_bg, (1280, 650))
        
        #icons joueurs :
        my_player = pg.image.load('icons/player_basic_image.png')
        self.player_icon = my_player.convert_alpha() # Pour gérer la transparence
        self.player_icon = pg.transform.scale(self.player_icon,(100,100))

        self.dictLevel = {"Chika": 0, "Luigi": 1, "Darth Limus": 2, "Patrick Cruel": 3}
        my_AIs = [pg.image.load(f"icons/player_AI_lv{lvl}.png") for lvl in range(1,5)]
        self.AI_icons = [my_ai.convert_alpha() for my_ai in my_AIs] # Pour gérer la transparence
        self.AI_icons = [pg.transform.scale(my_ai,(100,100)) for my_ai in self.AI_icons]

        playing_shape = pg.image.load('icons/playing_shape.png')
        self.playing_shape = playing_shape.convert_alpha() # Pour gérer la transparence
        self.playing_shape = pg.transform.scale(self.playing_shape,(100,100))        

        folded_shape = pg.image.load('icons/folded_shape.png')
        self.folded_shape = folded_shape.convert_alpha() # Pour gérer la transparence
        self.folded_shape = pg.transform.scale(self.folded_shape,(100,100))   

        winning_shape = pg.image.load('icons/winning_shape.png')
        self.winning_shape = winning_shape.convert_alpha() # Pour gérer la transparence
        self.winning_shape = pg.transform.scale(self.winning_shape,(100,100))  

        back_cards = pg.image.load('cards/back.png')
        self.back_cards = back_cards.convert_alpha()
        self.back_cards = pg.transform.scale(self.back_cards,(self.back_cards.get_width()//6.5,self.back_cards.get_height()//6.5))

        winning_card = pg.image.load('icons/winning_card.png')
        self.winning_card = winning_card.convert_alpha()
        self.winning_card = pg.transform.scale(self.winning_card,(self.winning_card.get_width()//6.5,self.winning_card.get_height()//6.5))

        self.client = client

        self.players_xy = [(430, 500),(780, 500),(1080, 250),(780, 40),(430, 40),(100, 250)] # liste des coordonnées de placement des joueurs autour de la table à déterminée

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
                    # # CHECK THE POSITION OF THE MOUSE
                    # mouse_pos = pg.mouse.get_pos()
                    # # CHECKING THE MOUSE CLICK EVENT
                    # mouse_click = pg.mouse.get_pressed()
                    button.handle_event(event)
                self.input_mise.handle_event(event)
                
            
            self.playRoom.blit(self.bg,(0,0))

            for button in input_buttons : 
                button.draw(self.playRoom)
             
            if self.client.me['isPlaying'] :
                self.input_mise.draw(self.playRoom)

            # Affichage du pot commun :

            text_pot = self.font.render("Pot : " + str(self.client.info['pot']), True, (0, 0, 128))
            textRect_pot = text_pot.get_rect()
            textRect_pot.center = (625,200)
            self.playRoom.blit(text_pot, textRect_pot)

            #affichage des cartes :
            board_cards = self.client.info['board']
            for i in range(len(board_cards)):
                img_card = pg.image.load('cards/'+board_cards[i]+'.png')
                (width, height) = img_card.get_size()
                img_card = pg.transform.scale(img_card,(width//5.5,height//5.5))
                img_card = img_card.convert_alpha()
                self.playRoom.blit(img_card,(400+100*i,250))

            my_cards = self.client.info['main'] 
            for i in range(len(my_cards)):
                img_card = pg.image.load('cards/'+my_cards[i]+'.png')
                (width, height) = img_card.get_size()
                img_card = pg.transform.scale(img_card,(width//6.5,height//6.5))
                img_card = img_card.convert_alpha()

                text_cards = self.font.render("Mes cartes", True, (0, 0, 128))
                textRect_cards = text_cards.get_rect()
                textRect_cards.center = (190,500)
                self.playRoom.blit(text_cards, textRect_cards)

                self.playRoom.blit(img_card,(100+100*i,530))
                
           # affichage joueurs :
            players = self.client.info['players']
            players = sorted(players, key=lambda x:x["id"])

            for k, player in enumerate(players) :
                if k in [0,1] :
                    offset = (-30,20)
                    offset_mise = (0,-50)
                    offset_cartes = [(25,-80),(51,-80)]
                    angle_cartes = 0
                elif k in [3,4] :
                    offset = (-50,50)
                    offset_mise = (0,130)
                    offset_cartes = [(25, 125),(51,125)]
                    angle_cartes = 180
                elif k == 5 :
                    offset = (50,130)
                    offset_mise = (160,30)
                    offset_cartes = [(150,50),(150,76)]
                    angle_cartes = 90
                else : 
                    offset = (50,120)
                    offset_mise = (-100,30)
                    offset_cartes = [(-100,50),(-100,76)]
                    angle_cartes = 270
                    
                pos = self.players_xy[k]

                if player['isAI'] :
                    idx = self.dictLevel[player['pseudo']]
                    self.playRoom.blit(self.AI_icons[idx], pos) 
                else :
                    self.playRoom.blit(self.player_icon, pos)

                if player['isPlaying'] :
                    self.playRoom.blit(self.playing_shape, pos)

                if player['id'] == self.client.abattage["won"] : 
                    self.playRoom.blit(self.winning_shape, pos)

                if player['folded'] : 
                    self.playRoom.blit(self.folded_shape, pos)
                else : 
                    img_rot = pg.transform.rotate(self.back_cards, angle_cartes)
                    # Affichage des cartes des joueurs
                    if self.client.abattage["won"] != -1 : 
                        cards = self.client.abattage[str(player['id'])]
                        for i in range(len(cards)) :
                            img_card = pg.image.load('cards/'+cards[i]+'.png')
                            img_card = pg.transform.scale(img_card,(self.back_cards.get_width(),self.back_cards.get_height()))
                            img_card = img_card.convert_alpha()
                            img_rot = pg.transform.rotate(img_card, angle_cartes)
                            self.playRoom.blit(img_rot, (pos[0] + offset_cartes[i][0],  pos[1] + offset_cartes[i][1]))
                        if player['id'] == self.client.abattage["won"]  :
                            winning_rot = pg.transform.rotate(self.winning_card, angle_cartes)
                            self.playRoom.blit(winning_rot, (pos[0] + offset_cartes[0][0],  pos[1] + offset_cartes[0][1]))
                            self.playRoom.blit(winning_rot, (pos[0] + offset_cartes[1][0],  pos[1] + offset_cartes[1][1]))
                    else : 
                        self.playRoom.blit(img_rot, (pos[0] + offset_cartes[0][0],  pos[1] + offset_cartes[0][1]))
                        self.playRoom.blit(img_rot, (pos[0] + offset_cartes[1][0],  pos[1] + offset_cartes[1][1]))

                

                text_pseudo = self.font.render(player['pseudo'], True, (0, 0, 128))
                textRect_pseudo = text_pseudo.get_rect()
                textRect_pseudo.center = (pos[0] + offset[0], pos[1] + offset[1])
                self.playRoom.blit(text_pseudo, textRect_pseudo)

                text_money = self.font.render(str(player['money']), True, (0, 0, 128))
                textRect_money = text_money.get_rect()
                textRect_money.center = (pos[0] + offset[0], pos[1] + offset[1]+30)
                self.playRoom.blit(text_money, textRect_money)

                text_mise = self.font.render(str(player['mise']), True, (0, 0, 128))
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
            clock.tick(60)

            if self.client.abattage["won"] != -1 :
                if next_turn:
                    pg.time.wait(3200)
                    self.client.abattage["won"] = -1 
                else:
                    next_turn = True
            else:
                next_turn = False
                
        pg.quit()
        return ""

