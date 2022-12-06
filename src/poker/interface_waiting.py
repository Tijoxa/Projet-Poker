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

        my_player = pg.image.load('icons/player_basic_image.png')
        self.player_icon = my_player.convert_alpha() # Pour gérer la transparence
        self.player_icon = pg.transform.scale(self.player_icon,(100,150))

        #connexion du joueur :
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
                
            # Affichage des clients connectés
            self.list_players = self.client.players[1:]
            font_pseudo = pg.font.Font('freesansbold.ttf', 32)
            for k in range (len(self.list_players)):
                # Affichage des icônes de personnage
                self.waiting.blit(self.player_icon, (50 + 160*k, 200))

                name = self.list_players[k].split("-")[1] # Obtention du nom du client à afficher
                text = font_pseudo.render(name, True, (0, 0, 128))
                textRect = text.get_rect()
                textRect.center = (100 + 150*k, 200)
                self.waiting.blit(text, textRect)

            # Réglage des joueurs attendus IA et réels 
            font_number = pg.font.Font('freesansbold.ttf', 32)
            N_IA_text = font_number.render(f"IAs : {str(self.client.N_players[1])}", True, (0, 0, 128))
            N_real_text = font_number.render(f"Joueurs : {str(self.client.N_players[0])}", True, (0, 0, 128))
            N_IA_textRect = N_IA_text.get_rect()
            N_real_textRect = N_real_text.get_rect()
            N_IA_textRect.center = (500, 400)
            N_real_textRect.center = (500, 460)
            self.waiting.blit(N_IA_text, N_IA_textRect)
            self.waiting.blit(N_real_text, N_real_textRect)
            
            #affichage du nbr de joueurs connectés :
            nbr_conn = f"connectés : {len(self.list_players)}/{int(self.client.N_players[0])+int(self.client.N_players[1])}"
            total_players = pg.font.Font('freesansbold.ttf', 28).render(nbr_conn, True, (0, 0, 128))
            total_players_Rect = total_players.get_rect()
            total_players_Rect.center = (500, 65)
            self.waiting.blit(total_players, total_players_Rect)
            

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