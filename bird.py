import pygame as pg

class Bird(pg.sprite.Sprite):
    def __init__(self):
        # inherit the bird class with sprite class-------------
        super(Bird, self).__init__()

        # open the images --------------
        self.sprite_list = [pg.transform.scale(pg.image.load(
            "Assets/Birdup.png"), (34, 30)), pg.transform.scale(pg.image.load("Assets/Birddown.png"), (34, 30))]
        self.image_index = 0
        self.image = self.sprite_list[self.image_index]
        self.rect = pg.Rect(80, 250, 34, 30)
        self.velocity=pg.Vector2((0,0))
        self.gravity=30
        
    # update the bird images and make the wings movable ------------------
    def update(self,dt):
        if self.image_index == 0:
            self.image_index = 1
            self.image = self.sprite_list[self.image_index]
        elif self.image_index == 1:
            self.image_index = 0
            self.image = self.sprite_list[self.image_index]

        self.velocity.y+=self.gravity*dt
        self.rect.y+=self.velocity.y

    def move(self,dt):
        self.velocity.y-=60*dt
