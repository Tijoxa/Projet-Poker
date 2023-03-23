import pygame as pg
from pygame.locals import *

from interface_elements import *

class GUI_loserRoom:
    def __init__(self):
        pg.init()
        #create the window :
        self.loserRoom = pg.display.set_mode([1280, 650])
        pg.display.set_caption("Poker ain't for Noobies")

        self.font_lost = pg.font.Font('freesansbold.ttf', 35)

        my_bg = pg.image.load('backgrounds/GameOver.jpeg')
        self.bg = pg.transform.scale(my_bg, (1280, 650))

    def mainloop(self):
        clock = pg.time.Clock()
        self.loserRoom.blit(self.bg,(0,0))

        text_lost = self.font_lost.render("Vous avez perdu !", True, (128, 60, 0))
        textRect_lost = text_lost.get_rect()
        textRect_lost.center = (640,525)
        self.loserRoom.blit(text_lost, textRect_lost)
        

        pg.display.flip()
        clock.tick(60)
        
        pg.time.wait(2600)
        pg.quit()
        return "HOME"

