import pygame as pg
from pygame.locals import *

from interface_elements import *
        
class GUI_homepage:
    def __init__(self):
        pg.init()
        #create the window :
        self.homepage = pg.display.set_mode([960, 720])
        pg.display.set_caption('Welcome in Centrale Poker')
        
        #background : https://www.casino-saint-julien.com/les-differents-types-de-poker/
        my_bg=pg.image.load('backgrounds/poker_background.jpg')
        self.bg = pg.transform.scale(my_bg, (960, 720))
        
        #create name entry box :
        self.input_name = InputBox(150, 600, 450, 48,
                                   text='name',
                                   centered=True)
        
        #create playstart button :
        self.play_button = Button(200, 150, 125, 50, (255, 250, 250),
                                 (255, 0, 0), "TimesNewRoman",
                                 (255, 255, 255), "Jouer !")
        
    def mainloop(self):
        clock = pg.time.Clock()
        input_boxes = [self.input_name]
        input_buttons = [self.play_button]
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                for box in input_boxes:
                    box.handle_event(event)
                for button in input_buttons :
                    button.handle_event(event)

            self.homepage.blit(self.bg,(0,0))
            
            for box in input_boxes:
                box.draw(self.homepage)
            for button in input_buttons : 
                button.draw(self.homepage)
                
            
            if self.play_button.CurrentState:
                self.play_button.CurrentState = False
                pg.quit()
                return "WAITING"
            pg.display.flip()
            clock.tick(30)
        pg.quit()
        return ""

