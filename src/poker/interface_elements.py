import pygame as pg
from pygame.locals import *

class InputBox:
    """class Input Box to modelize an entry text box"""
    def __init__(self, x, y, w = 200, h = 32, 
                 text='', textSize=None, textType = None,
                 color_active = 'black',
                 color_inactive = 'red',
                 centered=False):
        """
        initialization of an entry text box

        Parameters
        ----------
        x : int
            first coordinate pixel.
        y : int
            second coordinate pixel.
        w : int, optional
            wildth. The default is 200.
        h : int, optional
            height. The default is 32.
        text : string, optional
            initial text to show. The default is ''.
        textSize : int, optional
            size of the text, The default if the Box height
        textType : string, otional
            type of text, The default is system default
        color_active : string, optional
            color of the box if active. The default is 'black'.
        color_inactive : string, optional
            color of the box if inactive. The default is 'red'.
        centered : boolean, optional
            If True, the text is displayed in the center of the box. 
            The default is False.

        Returns
        -------
        None.

        """
        self.ow = w # save original width for update
        self.text = text
        self.COLOR_ACTIVE = pg.Color(color_active)
        self.COLOR_INACTIVE = pg.Color(color_inactive)
        self.color = self.COLOR_INACTIVE
        self.centered = centered
        self.FONT = pg.font.SysFont(textType, 
                                    size=h if textSize is None else textSize)
        self.rect = pg.Rect(x, y, w, h)
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def draw(self, screen, tickness = 2):
        text_w = self.txt_surface.get_width()
        # Resize the box if the text is too long.
        self.rect.w = max(self.ow, text_w +10)
        # Blit the text.
        if self.centered:
            screen.blit(self.txt_surface, 
                        (self.rect.x+(self.rect.w-text_w)//2, 
                         self.rect.y+5))
        else:
            screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
            
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, tickness)

class Button():
    # INITIALIZATION OF BUTTON COMPONENTS LIKE POSITION OF BUTTON,
    # COLOR OF BUTTON, FONT COLOR OF BUTTON, FONT SIZE, TEXT INSIDE THE BUTTON
    def __init__(self, x, y, sx, sy,
                 shape = 'rect',
                 colour_mouse_on = 'black', colour_mouse_off = 'red', 
                 textType = "TimeNewRoman", textColour = 'white', 
                 textSize = 25, text = "..."):
        """
        Generate button

        Parameters
        ----------
        x : int
            x origin.
        y : int
            y origin.
        sx : int
            width.
        sy : int
            height.
        shape : string, optional
            type shape of the button. Can rectangular (rect),
            or circular (circle). The default is 'rect'.
        colour_mouse_on : string, optional
            button colour when the mouse is on it. The default is 'black'.
        colour_mouse_off : string, optional
            button colour when the house is off it. The default is 'red'.
        textType : string, optional
            DESCRIPTION. The default is "TimeNewRoman".
        textColour : string, optional
            colour of the text. The default is 'white'.
        text : string, optional
            text displayed in the button. The default is "...".

        Returns
        -------
        None.

        """
        # origin coordinates :
        self.x = x
        self.y = y
        # last coordinates :
        self.sx = sx
        self.sy = sy
        # Colours possible deponding on mouse position :
        self.COLOR_INACTIVE = pg.Color(colour_mouse_off)
        self.COLOR_ACTIVE = pg.Color(colour_mouse_on)
        self.fbcolour = self.COLOR_INACTIVE #couleur actuelle
        # text :
        self.tcolour = pg.Color(textColour)
        self.text = text
        self.fontsize = textSize
        self.buttonf = pg.font.SysFont(textType, self.fontsize)
        # CURRENT IS OFF
        self.CurrentState = False
        # COLLIDER FOR THE CLICK CHECKING
        self.shape = shape 
        self.rect = pg.Rect(x, y, sx, sy)

 
    def handle_event(self, event):
        #change color if mouse on button : 
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.fbcolour=self.COLOR_ACTIVE
        else:
            self.fbcolour = self.COLOR_INACTIVE
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.CurrentState = True
            else:
                self.CurrentState = False
                
    # DRAW THE BUTTON
    def draw(self, display, tickness = 0):
        # RENDER THE FONT OBJECT FROM THE STSTEM FONTS
        textsurface = self.buttonf.render(self.text,
                                          False, self.tcolour)
 
        # THIS LINE WILL DRAW THE SURF ONTO THE SCREEN
        if self.shape == 'rect':
            pg.draw.rect(display, self.fbcolour, self.rect, tickness)
        elif self.shape == 'circle':
            pg.draw.ellipse(display, self.fbcolour,self.rect, tickness)
            
        display.blit(textsurface,
                 (self.x + (self.sx - textsurface.get_width())//2,
                  self.y + (self.sy - self.fontsize)//2))
 

class Player_display:
    """Class medelizing a player around the table"""
    def __init__(self, x, y, w, h, 
                 pseudo, isAI, player_info,
                 textType = "TimeNewRoman",
                 textSize = 25):
        
        #coordonnées :
        self.x, self.y, self.w, self.h = x,y,w,h
        #player_info contient les infos du joueur qui doivent être mises à jour.
        self.player_info = player_info
        #infos constantes du joueur :
        self.isAI=isAI
        self.name = pseudo
        
        #creation des fonts d'affichage du pseudo et de l'argent :
        self.pseudo = pg.font.SysFont(textType, textSize)
        self.money = pg.font.SysFont(textType, textSize)
        
        #affichage des cartes :
            ### TODO : afficher les cartes ###
            
        #creation des boutons si le joueur est humain:
        if not self.isAI:
            call = Button()
            check = Button()
            fold = Button()
            raise_ = Button()
            bet = Button()
            #creation de l'entrée de mise :
            bet_entry = InputBox()
        
            
            
    def draw(self, screen):
        if self.player_info.isPlaying and not self.isAI:
            pass
    def update_player_info(self,data):
        #mise à jour des infos du joueur en fonction des infos du server
        pass
        