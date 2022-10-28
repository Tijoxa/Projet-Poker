import pygame as pg
from pygame.locals import *

from interface_elements import *
        
class GUI_homepage:
    def __init__(self):
        pg.init()
        #create the window :
        self.homepage = pg.display.set_mode([640, 480])
        
        #create name entry box :
        self.input_name = InputBox(100, 400, 300, 32,'name')
        
    def mainloop(self):
        clock = pg.time.Clock()
        input_box1 = self.input_name
        input_boxes = [input_box1]
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            self.homepage.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(self.homepage)

            pg.display.flip()
            clock.tick(30)
        pg.quit()

gui = GUI_homepage()
gui.mainloop()