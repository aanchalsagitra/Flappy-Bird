import pygame as pg 
import random
class Pipe(pg.sprite.Sprite):

    def __init__(self,position,last_pipe_right,last_pipe_bottom=None):
        super(Pipe,self).__init__()

        self.gap=180
        # for upper pipe------------------------
        if position==1:
            self.image = pg.transform.scale(pg.transform.flip(pg.image.load("Assets/pipe.png"),False,True),(40,200))
            self.rect =self.image.get_rect()
            self.rect.top=random.randint(-150,0)
        # for lower pipe-----------------------------
        else:
             self.image = pg.transform.scale(pg.image.load("Assets/pipe.png"),(40,300))
             self.rect =self.image.get_rect()
             self.rect.top=last_pipe_bottom+self.gap
        self.rect.left=last_pipe_right+150
        
