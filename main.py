import pygame as pg
from pygame import mixer
import sys
import time
from bird import Bird
from pipe import Pipe

# initialize the pygame 
pg.init()
mixer.init()
clock = pg.time.Clock()

#display window--------------------------
width = 500
height = 600
display_window = pg.display.set_mode((width, height))
pg.display.set_caption("Flappy Bird Game")

# background image on display window------------------
background_image = pg.transform.scale(
    (pg.image.load("Assets/bg.png")), (width, height))
background_image_rect = background_image.get_rect()

# base image on display window --------------------------
base_image = pg.transform.scale((pg.image.load("Assets/base.png")), (width+30, 100))
base_image_rect = base_image.get_rect()
base_image_rect.y = height-100

#creating a music 
score_sound=pg.mixer.Sound("Assets/scoregain.mp3")
die_sound=pg.mixer.Sound("Assets/die.mp3")

# check the position of bird whether it is in the pipe or not ---------------------
start_monitor=False

#make the score object and score label-------------------
score=0
score_font=pg.font.Font("Assets/GARABD.ttf",26)
score_label=score_font.render("Score:0",(0,0,0),(0,0,0))
score_rect=score_label.get_rect()
score_rect.center=(60,20)

#make the game over object and game over label-------------------
game_over_font=pg.font.Font("Assets/GARABD.ttf",22)
game_over_label=game_over_font.render("Game Over",(0,0,0),(0,0,0))
game_over_rect=game_over_label.get_rect()
game_over_rect.center=(250,550)

#make the restart button and restart label-------------------
restart_font=pg.font.Font("Assets/GARABD.ttf",22)
restart_label=restart_font.render("Restart",(0,0,0),(0,0,0))
restart_rect=restart_label.get_rect()
restart_rect.center=(250,580)

# check the collision of bird with pipe and the base --------------
def birdCollision(bird_object,pipes):
    if bird_object.rect.y < 0:
        bird_object.velocity.y = 0
    elif bird_object.rect.y > 475: 
        bird_object.velocity.y = 0
        bird_object.gravity = 0
        pg.mixer.Sound.play(die_sound)
        pg.mixer.music.stop()
        return True
        
    if bird_object.rect.colliderect(pipes[0].rect) or bird_object.rect.colliderect(pipes[1].rect):
        pg.mixer.Sound.play(die_sound)
        pg.mixer.music.stop()
        return True
    return False 

# checking the score and modifying it ----------
def checkScore(bird_object,pipe):
    global score,start_monitor,score_label,score_sound
    if start_monitor==False:
        if bird_object.rect.left>pipe.rect.left and bird_object.rect.right<pipe.rect.right:
            start_monitor=True
    elif start_monitor==True:
        if bird_object.rect.left>pipe.rect.right:
            start_monitor=False
            score+=1
            score_label=score_font.render(f"Score:{score}",(0,0,0),(0, 0, 0))
            pg.mixer.Sound.play(score_sound)
            pg.mixer.music.stop()

def main():
    global score,base_image_rect, start_monitor,score_label,score_font
    run =True
    bird_object = Bird()
    pipes_list = []
    start_monitor=False
    score=0 
    game_over=False

    last_time = time.time()

    while run:
        # check the events-----------------------
        for events in pg.event.get():
            if events.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif events.type==pg.MOUSEBUTTONDOWN and game_over==True:
                mousepos=events.pos
                if restart_rect.collidepoint(mousepos):
                    score_label=score_font.render(f"Score:0",(0,0,0),(0, 0, 0))
                    run=False

        #If game is not yet over then keep doing these things  
        if game_over==False:
            
            # creating the delta time ------------------------
            new_time = time.time()
            dt = new_time-last_time
            last_time = new_time
            
            # make the first pipe on display window ----------------
            if len(pipes_list) == 0:
                temp_list=[]
                temp_list.append(Pipe(1,500))
                temp_list.append(Pipe(-1,500,temp_list[0].rect.bottom))
                pipes_list.append(temp_list)
            # append the pipes in the list ------------------
            elif len(pipes_list) <= 3:
                temp_list=[]
                temp_list.append(Pipe(1,pipes_list[-1][0].rect.right))
                temp_list.append(Pipe(-1,pipes_list[-1][0].rect.right,temp_list[0].rect.bottom))
                pipes_list.append(temp_list)
                

            # check which key is pressed by the user------------
            keys = pg.key.get_pressed()
            if keys[pg.K_SPACE]:
                bird_object.move(dt)

            # fill the display window and blit the background image --------------
            display_window.fill((255, 255, 255))
            display_window.blit(background_image, background_image_rect)

            # moving the pipes and deleting the pipe which is on 0th index ----------
            for pipes in pipes_list:
                pipes[0].rect.x -= 60*dt
                pipes[1].rect.x -= 60*dt
            if pipes_list[0][0].rect.left <= 0:
                pipes_list.pop(0)
                
            #moving the base image-----------------
            if base_image_rect.x <= -30:
                base_image_rect.x = 0
            else:
                base_image_rect.x -= 150*dt

            # calling the collision function ------------
            game_over=birdCollision(bird_object,pipes_list[0])

            #calling the score function
            checkScore(bird_object,pipes_list[0][0])
            
            #blit the upper and lower pipe on the display window---------
            for pipes in pipes_list:
                display_window.blit(pipes[0].image, pipes[0].rect)
                display_window.blit(pipes[1].image, pipes[1].rect)
                
            #blit the score and base image on the screen---------------
            display_window.blit(score_label,score_rect)
            display_window.blit(base_image, base_image_rect)

            # check whether the game is over or not -----------
            if game_over==True:
                display_window.blit(game_over_label,game_over_rect)
            bird_object.update(dt)

            display_window.blit(bird_object.image, bird_object.rect)
        
        # restart condition ----------------------
        elif game_over==True:
                # pg.mixer.Sound.play(die_sound)
                display_window.blit(restart_label,restart_rect)
                # pg.mixer.music.stop()
         
        pg.display.update()
        clock.tick(60)
    #calling the main function again
    main()
main()
