import pygame as pg
from pygame.locals import *


class InputBox:
    def __init__(self, x, y, w, h, text='',
                 color_active = 'orange',
                 color_inactive = 'red',
                 centered=False):
        self.COLOR_INACTIVE = pg.Color(color_active)
        self.COLOR_ACTIVE = pg.Color(color_inactive)
        self.color = self.COLOR_INACTIVE
        self.centered = centered
        self.FONT = pg.font.Font(None, 32)
        self.rect = pg.Rect(x, y, w, h)
        self.ow = w # save original width for update
        self.text = text
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

    def draw(self, screen):
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
        pg.draw.rect(screen, self.color, self.rect, 2)

class Button():
    # INITIALIZATION OF BUTTON COMPONENTS LIKE POSITION OF BUTTON,
    # COLOR OF BUTTON, FONT COLOR OF BUTTON, FONT SIZE, TEXT INSIDE THE BUTTON
    def __init__(self, x, y, sx, sy, bcolour,
                 fbcolour, font, fcolour, text):
        # ORIGIN_X COORDINATE OF BUTTON
        self.x = x
        # ORIGIN_Y COORDINATE OF BUTTON
        self.y = y
        # LAST_X COORDINATE OF BUTTON
        self.sx = sx
        # LAST_Y COORDINATE OF BUTTON
        self.sy = sy
        # FONT SIZE FOR THE TEXT IN A BUTTON
        self.fontsize = 25
        # BUTTON COLOUR
        self.bcolour = bcolour
        # RECTANGLE COLOR USED TO DRAW THE BUTTON
        self.fbcolour = fbcolour
        # BUTTON FONT COLOR
        self.fcolour = fcolour
        # TEXT IN A BUTTON
        self.text = text
        # CURRENT IS OFF
        self.CurrentState = False
        # FONT OBJECT FROM THE SYSTEM FONTS
        self.buttonf = pg.font.SysFont(font, self.fontsize)
        # COLLIDER FOR THE CLICK CHECKING
        self.rect = pg.Rect(x, y, sx, sy)

 
    # DRAW THE BUTTON
    def showButton(self, display):
        pg.draw.rect(display, self.fbcolour,
                     (self.x, self.y,
                     self.sx, self.sy))
        # RENDER THE FONT OBJECT FROM THE STSTEM FONTS
        textsurface = self.buttonf.render(self.text,
                                          False, self.fcolour)
 
        # THIS LINE WILL DRAW THE SURF ONTO THE SCREEN
        display.blit(textsurface,
                     ((self.x + (self.sx/2) -
                       (self.fontsize/2)*(len(self.text)/2) + 10
                       , (self.y + (self.sy/2) -
                           (self.fontsize/2)-4))))
 
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.CurrentState = True
            else:
                self.active = False
        