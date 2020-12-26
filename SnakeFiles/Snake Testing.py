#Snake

#Imported Libraries

import pygame
import random
import numpy as np
import time
import math
import tkinter as tk
from tkinter import messagebox
pygame.init()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Random Shit

#Res Must 16:9

#Hard Coded Dummy Constants
screen_width = 1920
screen_height = 1080
columns = 64
rows = 36
orient = None

#Character Info
block_width = screen_width / columns
block_height = screen_height / rows
x = block_width
y = block_height
character_coord = (x,y)
vel = block_height
move_list = [(x,y,orient)]
m = 1

#Character Graphics

#Head
headU = pygame.image.load('Graphics/SnakeHeadU.png')
headD = pygame.image.load('Graphics/SnakeHeadD.png')
headR = pygame.image.load('Graphics/SnakeHeadR.png')
headL = pygame.image.load('Graphics/SnakeHeadL.png')

#Body
bodyU = pygame.image.load('Graphics/SnakeBodyU.png')
bodyD = pygame.image.load('Graphics/SnakeBodyD.png')
bodyR = pygame.image.load('Graphics/SnakeBodyR.png')
bodyL = pygame.image.load('Graphics/SnakeBodyL.png')

#Tail
tailU = pygame.image.load('Graphics/SnakeTailU.png')
tailD = pygame.image.load('Graphics/SnakeTailD.png')
tailR = pygame.image.load('Graphics/SnakeTailR.png')
tailL = pygame.image.load('Graphics/SnakeTailL.png')

#Window Info
pygame.display.set_caption("Snake")
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #pygame.display.set_mode((screen_width,screen_height))
window.fill((97,70,21))
pygame.display.update()

#Snack Info
snackonscreen = False
x_coord = 0
y_coord = 0
snack_coord = (x_coord,y_coord)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Functions Defined

def redrawWindow():
    character = pygame.draw.rect(window, (255,0,0), (x,y,block_width,block_height))
    pygame.display.update(character)
    if keys[pygame.K_ESCAPE]:
        pygame.display.set_mode((screen_width,screen_height))

def snack():
    global snackonscreen, snack_coord, x_coord, y_coord
    if snackonscreen == False:
        x_coord = block_width * random.randint(0,63)
        y_coord = block_height * random.randint(0,35)
        snack_coord = (x_coord,y_coord)
        snackonscreen = True

def printsnack():
    global x_coord, y_coord
    snack()
    snackdrop = pygame.draw.rect(window, (0,255,0), (x_coord,y_coord,block_width,block_height))
    pygame.display.update(snackdrop)

def tracker():
    if (x_coord == x) and (y_coord == y):
        move_list.append((x,y,orient))
    else:
        a = int(move_list[0][0])
        b = int(move_list[0][1])
        tracker = pygame.draw.rect(window, (97,70,21), (a,b,block_width,block_height))
        pygame.display.update(tracker)
        move_list.append((x,y,orient))
        del move_list[0]

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Main Run

run = True
while run:
    pygame.time.delay(100)  #create delay on every action

    keys = pygame.key.get_pressed() #read keys 

    if (keys[pygame.K_LEFT] and x != 0) or (keys[pygame.K_a] and x != 0): #move left(1)
        x -= vel
        orient = L
        tracker()

    elif (keys[pygame.K_RIGHT]and x != screen_width - block_width) or (keys[pygame.K_d]and x != screen_width - block_width): #move right(2)
        x += vel
        orient = R
        tracker()

    elif (keys[pygame.K_UP] and y != 0) or (keys[pygame.K_w] and y != 0): #move up(3)
        y -= vel
        orient = U
        tracker()

    elif (keys[pygame.K_DOWN] and y != screen_height - block_height) or (keys[pygame.K_s] and y != screen_height - block_height): #move down(4)
        y += vel
        orient = D
        tracker()

    redrawWindow()

    if (x_coord == x) and (y_coord == y):
        snackonscreen = False
        m += 1

    if snackonscreen == False:
        printsnack()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit by clicking "X" button with no error
            run = False
    
pygame.quit()