import pygame as pg
from pygame.locals import *


class InputBox:
    def __init__(self, x, y, w, h, text='',
                 color_active = 'dodgerblue2',
                 color_inactive = 'lightskyblue3'):
        self.COLOR_INACTIVE = pg.Color(color_active)
        self.COLOR_ACTIVE = pg.Color(color_inactive)
        self.FONT = pg.font.Font(None, 32)
        self.rect = pg.Rect(x, y, w, h)
        self.ow = w # save original width for update
        self.color = self.COLOR_INACTIVE
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

    def update(self):
        # Resize the box if the text is too long.
        self.rect.w = max(self.ow, self.txt_surface.get_width()+10)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

