import pygame as pg
from pygame.locals import *

from interface_elements import *

class GUI_waiting:
    def __init__(self, client):
        pg.init()
        #create the window :
        self.waiting = pg.display.set_mode([1023, 510])
        self.max_players = 6 # Pour limiter le nombre de joueurs dans les sélecteurs de la salle d'attente
        pg.display.set_caption("Salle d'attente")
        
        #background : 
        my_bg = pg.image.load('backgrounds/waiting_background.png')
        self.bg = pg.transform.scale(my_bg, (1023, 510))
        
        self.client = client

        #connected players : 
        self.list_players = []
        
        #icons joueurs :
        my_player = pg.image.load('icons/player_basic_image.png')
        self.player_icon = my_player.convert_alpha() # Pour gérer la transparence
        self.player_icon = pg.transform.scale(self.player_icon,(100,100))

        my_open = pg.image.load('icons/player_open_image.png')
        self.open_icon = my_open.convert_alpha() # Pour gérer la transparence
        self.open_icon = pg.transform.scale(self.open_icon,(100,100))

        my_AIs = [pg.image.load(f"icons/player_AI_lv{lvl}.png") for lvl in range(1,5)]
        self.AI_icons = [my_ai.convert_alpha() for my_ai in my_AIs] # Pour gérer la transparence
        self.AI_icons = [pg.transform.scale(my_ai,(100,100)) for my_ai in self.AI_icons]

        
        #boutons :
        self.button_quit = Button(20, 30, 200, 50, text = "Quitter la salle")
        self.button_play = Button(800, 30, 200, 50, text = "Lancer la partie !")
        #boutons d'admin :
        self.button_add_IA = Button(570, 375, 50, 50, shape = 'circle',
                                       colour_mouse_on = 'black', colour_mouse_off = 'green',
                                       textSize = 30, text = "+")
        self.button_del_IA = Button(380, 375, 50, 50, shape = 'circle',
                                       colour_mouse_on = 'black',
                                       textSize = 30, text = "-")
        self.button_add_player = Button(600, 435, 50, 50, shape = 'circle',
                                       colour_mouse_on = 'black', colour_mouse_off = 'green',
                                       textSize = 30, text = "+")
        self.button_del_player = Button(360, 435, 50, 50, shape = 'circle',
                                       colour_mouse_on = 'black',
                                       textSize = 30, text = "-")
        self.ia_buttons = [Button(79 + 160*k, 125, 40,40,  shape = 'circle',
                                       colour_mouse_on = 'black', colour_mouse_off = 'purple',
                                       textSize = 30, text = "1") for k in range(6)]
    def mainloop(self):
        clock = pg.time.Clock()
        done = False
        
        while not done:

            if self.client.isAdmin:
                input_buttons = [self.button_quit,self.button_play, 
                                self.button_add_player, self.button_del_player,
                                self.button_add_IA, self.button_del_IA, self.button_play]
            else:
                input_buttons = [self.button_quit]

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                for button in input_buttons :
                    # # CHECK THE POSITION OF THE MOUSE
                    # mouse_pos = pg.mouse.get_pos()
                    # # CHECKING THE MOUSE CLICK EVENT
                    # mouse_click = pg.mouse.get_pressed()
                    button.handle_event(event)
                for ia_button in self.ia_buttons:
                    ia_button.handle_event(event)

            self.waiting.blit(self.bg,(0,0))
            for button in input_buttons : 
                button.draw(self.waiting)

            N_joueurs = int(self.client.N_players[0])
            N_reel = len(self.list_players)
            N_IAs = int(self.client.N_players[1])
            if self.client.isAdmin:
                for ia_button in self.ia_buttons[N_reel:N_reel+N_IAs]:
                    ia_button.draw(self.waiting)
                
            # Affichage des clients connectés
            self.list_players = self.client.players
            font_pseudo = pg.font.Font('freesansbold.ttf', 32)
            for k in range (len(self.list_players)):
                self.waiting.blit(self.player_icon, (50 + 160*k, 250)) # Affichage des icônes de personnage

                name = self.list_players[k].split("-")[1] # Obtention du nom du client à afficher
                text = font_pseudo.render(name, True, (0, 0, 128))
                textRect = text.get_rect()
                textRect.center = (100 + 150*k, 200)
                self.waiting.blit(text, textRect)

            # Affichage des IAs (elles ne sont pas encore connectées, mais affichées à titre informatif)
            N = len(self.list_players) 
            Ai_levels = [int(lvl) for lvl in self.client.N_players[2:]]
            for k in range (int(self.client.N_players[1])):
                self.waiting.blit(self.AI_icons[Ai_levels[k]-1], (50 + 160*(k + N), 250)) # Affichage des icônes de personnage
                name = "IA-" + str(k) # Obtention du nom de l'IA à afficher
                text = font_pseudo.render(name, True, (0, 0, 128))
                textRect = text.get_rect()
                textRect.center = (100 + 160*(k + N), 200)
                self.waiting.blit(text, textRect)

            # Affichage des créneaux ouverts
            N_connected = len(self.list_players) + N_IAs
            for k in range (N_joueurs - N):
                self.waiting.blit(self.open_icon, (50 + 160*(k + N_connected), 250)) # Affichage des icônes de personnage

            # Réglage des joueurs attendus IA et réels 
            font_number = pg.font.Font('freesansbold.ttf', 32)
            N_IA_text = font_number.render(f"IAs : {N_IAs}", True, (0, 0, 128))
            N_real_text = font_number.render(f"Joueurs : {N_joueurs}", True, (0, 0, 128))
            N_IA_textRect = N_IA_text.get_rect()
            N_real_textRect = N_real_text.get_rect()
            N_IA_textRect.center = (500, 400)
            N_real_textRect.center = (500, 460)
            self.waiting.blit(N_IA_text, N_IA_textRect)
            self.waiting.blit(N_real_text, N_real_textRect)

            # Affichage du nbr de joueurs connectés :
            nbr_conn = f"connectés : {len(self.list_players)}/{N_joueurs+ N_IAs}"
            total_players = pg.font.Font('freesansbold.ttf', 28).render(nbr_conn, True, (0, 0, 128))
            total_players_Rect = total_players.get_rect()
            total_players_Rect.center = (500, 65)
            self.waiting.blit(total_players, total_players_Rect)
            
            if self.button_quit.CurrentState:
                self.button_quit.CurrentState = False
                pg.quit()
                return "HOME"

            if self.client.ready_for_game :
                pg.quit()
                return "PLAY"

            if self.client.isAdmin:
                if self.button_play.CurrentState:
                    self.button_play.CurrentState = False
                    self.client.waiting_for_game = True

                if self.button_del_IA.CurrentState:
                    self.button_del_IA.CurrentState = False
                    self.client.N_players[1] = str(max(0, N_IAs -1))
                    if len(self.client.N_players) > 2:
                        self.client.N_players = self.client.N_players[:-1]

                if self.button_del_player.CurrentState:
                    self.button_del_player.CurrentState = False
                    self.client.N_players[0] = str(max(len(self.list_players),N_joueurs -1))

                if self.button_add_IA.CurrentState:
                    self.button_add_IA.CurrentState = False
                    self.client.N_players[1] = str(min( max(0,int(self.client.N_players[1]) +1),self.max_players - int(self.client.N_players[0]))) # Min-max pour borner entre 0 et self.max_players 
                    if len(self.client.N_players) < self.max_players - int(self.client.N_players[0]) + 2 :
                        self.client.N_players.append("1")

                if self.button_add_player.CurrentState:
                    self.button_add_player.CurrentState = False
                    self.client.N_players[0] = str(min(max(0,int(self.client.N_players[0]) +1),self.max_players - int(self.client.N_players[1])))
            
                for k in range(N_reel,N_reel+N_IAs):
                    if  self.ia_buttons[k].CurrentState:
                        self.ia_buttons[k].CurrentState = False
                        niveau =  int(self.ia_buttons[k].text) % 4 + 1
                        self.ia_buttons[k].text = str(niveau)
                        self.client.N_players[2+k-N_reel] = str(niveau)
            pg.display.flip()
            pg.display.update()
            clock.tick(30)
        pg.quit()
        return ""