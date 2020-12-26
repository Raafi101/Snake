#Snake

#Imported Libraries

import pygame
import random
import time
import math
pygame.init()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Random Shit

titlefont = pygame.font.SysFont('comicsansms', 40, 1)
ingamefont = pygame.font.SysFont('comicsansms', 30)

#Res Must 16:9

#Hard Coded Dummy Constants
screen_width = 900
screen_height = 1000
columns = 30
rows = 30
orient = None
U = 8
D = 5
R = 6
L = 4

#Character Info
block_width = screen_width / columns
block_height = screen_width / rows
x = block_width
y = (block_height + 100)
character_coord = (x,y)
vel = block_width
move_list = [(x,y,orient)]
m = 1
score = 0

#Graphics

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

#Snack
apple = pygame.image.load('Graphics/Apple.png')

#Window Info
pygame.display.set_caption("Snake")
window = pygame.display.set_mode((900, 1000)) #pygame.display.set_mode((screen_width,screen_height))
window.fill((27,94,31))
pygame.display.update()

#Snack Info
snackonscreen = False

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Functions Defined

#Buttons Class
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsansms', 40)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

#Character
def redrawCharacter():
    if orient == U:
        character = window.blit(headU, (x,y))
        pygame.display.update(character)
    elif orient == D:
        character = window.blit(headD, (x,y))
        pygame.display.update(character)
    elif orient == R:
        character = window.blit(headR, (x,y))
        pygame.display.update(character)
    elif orient == L:
        character = window.blit(headL, (x,y))
        pygame.display.update(character)

def snack():
    global snackonscreen, snack_coord, x_coord, y_coord
    if snackonscreen == False:
        x_coord = block_width * random.randint(0,29)
        y_coord = (block_height * random.randint(0,29)) + 100
        snack_coord = (x_coord,y_coord, orient)
        if (x_coord, y_coord, U) in move_list or (x_coord, y_coord, D) in move_list or (x_coord, y_coord, R) in move_list or (x_coord, y_coord, L) in move_list:
            snack()
        else:
            snackonscreen = True

def printsnack():
    global x_coord, y_coord, snackdrop
    snack()
    snackdrop = window.blit(apple, (x_coord, y_coord))
    pygame.display.update(snackdrop)

def tracker():
    global score
    if (x_coord == x) and (y_coord == y):
        move_list.append((x,y,orient))
    else:
        a = int(move_list[0][0])
        b = int(move_list[0][1])
        tracker = pygame.draw.rect(window, (27,94,31), (a,b,block_width,block_height))
        pygame.display.update(tracker)
        move_list.append((x,y,orient))
        del move_list[0]

def painter():
    #clearer
    if (x_coord == x) and (y_coord == y):
        for q in (0,m-1):
            clearer = pygame.draw.rect(window, (27,94,31), (move_list[q][0],move_list[q][1],block_width,block_height))
            pygame.display.update(clearer)
    else:
        for q in (0,m-2):
            clearer = pygame.draw.rect(window, (27,94,31), (move_list[q][0],move_list[q][1],block_width,block_height))
            pygame.display.update(clearer)

def scoretracker():
    global score
    score = m - 2
    banner = pygame.draw.rect(window, (8,71,12), (0,0,900,100))
    pygame.display.update(banner)
    score_count = ingamefont.render("Score: " + str(score) + " ", 2, (255,255,255), None)
    direcs = ingamefont.render("Use W,A,S,D / arrows keys to move.", 2, (255,255,255), None)
    direcs_render = window.blit(direcs, (block_width, .8*block_height))
    score_render = window.blit(score_count, (screen_width - 7*block_width, .8*block_height))
    pygame.display.update(score_render)
    pygame.display.update(direcs_render)
        
def boundary():
    if (x < 0) or (x > screen_width - block_width) or (y < 100) or (y > screen_height - block_height):
        window.fill((27,94,31))
        pygame.display.update()
        scoretracker()
        loss = titlefont.render("YOU LOST!", 1, (255,255,255))
        loss_render = window.blit(loss, (11.5*block_width, 7*block_height))
        pygame.display.update(loss_render)
        time.sleep(3)
        run = False
        mainmenu()

    if m == 900:
        window.fill((27,94,31))
        pygame.display.update()
        scoretracker()
        win = titlefont.render("YOU WON!", 1, (255,255,255))
        win_render = window.blit(win, (11.5*block_width, 7*block_height))
        pygame.display.update(win_render)
        time.sleep(3)
        run = False
        mainmenu()
    
    for e in range(m-1):
        if ((x == move_list[e][0]) and (y == move_list[e][1])):
            window.fill((27,94,31))
            pygame.display.update()
            scoretracker()
            loss = titlefont.render("YOU LOST!", 1, (255,255,255))
            loss_render = window.blit(loss, (11.5*block_width, 7*block_height))
            pygame.display.update(loss_render)
            time.sleep(3)
            run = False
            mainmenu()
        else:
            pass

    #body painter
    if m > 2:
        if (x_coord == x) and (y_coord == y):
            for p in (1,m-1):
                if move_list[p][2] == U:
                    body_p = window.blit(bodyU, (move_list[p][0],move_list[p][1]))
                    pygame.display.update(body_p)
                if move_list[p][2] == D:
                    body_p = window.blit(bodyD, (move_list[p][0],move_list[p][1]))
                    pygame.display.update(body_p)
                if move_list[p][2] == R:
                    body_p = window.blit(bodyR, (move_list[p][0],move_list[p][1]))
                    pygame.display.update(body_p)
                if move_list[p][2] == L:
                    body_p = window.blit(bodyL, (move_list[p][0],move_list[p][1]))
                    pygame.display.update(body_p)
        else:
            for p in (1,m-2):
                if move_list[p][2] == U:
                    body_p = window.blit(bodyU, (move_list[p][0],move_list[p][1]))
                    pygame.display.update(body_p)
                if move_list[p][2] == D:
                    body_p = window.blit(bodyD, (move_list[p][0],move_list[p][1]))
                    pygame.display.update(body_p)
                if move_list[p][2] == R:
                    body_p = window.blit(bodyR, (move_list[p][0],move_list[p][1]))
                    pygame.display.update(body_p)
                if move_list[p][2] == L:
                    body_p = window.blit(bodyL, (move_list[p][0],move_list[p][1]))
                    pygame.display.update(body_p)

    #tail painter
    if m > 1:
        if move_list[0][2] == U:
            tail = window.blit(tailU, (move_list[0][0],move_list[0][1]))
            pygame.display.update(tail)
        elif move_list[0][2] == D:
            tail = window.blit(tailD, (move_list[0][0],move_list[0][1]))
            pygame.display.update(tail)
        elif move_list[0][2] == R:
            tail = window.blit(tailR, (move_list[0][0],move_list[0][1]))
            pygame.display.update(tail)
        elif move_list[0][2] == L:
            tail = window.blit(tailL, (move_list[0][0],move_list[0][1]))
            pygame.display.update(tail)

def rungame():
    global m, x, y, snackonscreen, orient, keys

    x += vel
    orient = R
    tracker()

    run = True
    while run:
        window.fill((27,94,31))

        pygame.time.delay(100)  #create delay on every action

        keys = pygame.key.get_pressed() #read keys

        if (keys[pygame.K_RIGHT]) or (keys[pygame.K_d]):
            x += vel
            orient = R
            tracker()
            painter()
        
        elif (keys[pygame.K_LEFT]) or (keys[pygame.K_a]): #move left(1)
            x -= vel
            orient = L
            tracker()
            painter()

        elif (keys[pygame.K_UP]) or (keys[pygame.K_w]): #move up(3)
            y -= vel
            orient = U
            tracker()
            painter()
        
        elif (keys[pygame.K_DOWN]) or (keys[pygame.K_s]): #move down(4)
            y += vel
            orient = D
            tracker()
            painter()

        scoretracker()
        redrawCharacter()
        boundary()

        if (x_coord == x) and (y_coord == y):
            snackonscreen = False
            m += 1

        if snackonscreen == False:
            printsnack()

        if keys[pygame.K_ESCAPE]:
            run = False
            mainmenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quit by clicking "X" button with no error
                run = False
                pygame.quit()

def mainmenu():
    global orient, U, D, R, L, x, y, character_coord, vel, move_list, m, x_coord, y_coord, score, screen_width, screen_height, block_height, block_width, snackdrop
    menu = True
    while menu:
        window.fill((27,94,31))
        Title = titlefont.render("SNAKE by Raafi Rahman", 1, (255,255,255))
        Title_render = window.blit(Title, (7.5*block_width, block_height))
        pygame.display.update(Title_render)

        PlayButton = button((148,18,18), 10*block_width, 6*block_height, 10*block_width, 2*block_height, 'Play')
        Play_button = PlayButton.draw(window, (0,0,0))

        ExitButton = button((148,18,18), 10*block_width, 10*block_height, 10*block_width, 2*block_height, 'Exit')
        Exit_button = ExitButton.draw(window, (0,0,0))

        pygame.display.update()
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT: #quit by clicking "X" button with no error
                menu = False
                pygame.quit()

            pos = pygame.mouse.get_pos() #Mouse clicks on screen
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if PlayButton.isOver(pos):
                    pygame.display.flip()
                    window.fill((27,94,31)) 
                    pygame.display.update()

                    screen_width = 900
                    screen_height = 1000
                    columns = 30
                    rows = 30
                    orient = None
                    U = 8
                    D = 5
                    R = 6
                    L = 4

                    block_width = screen_width / columns
                    block_height = screen_width / rows
                    x = block_width
                    y = block_height + 100
                    character_coord = (x,y)
                    vel = block_height
                    move_list = [(x,y,orient)]
                    m = 1
                    score = 0

                    x_coord = 60
                    y_coord = 130
                    snackdrop = window.blit(apple, (x_coord, y_coord))
                    pygame.display.update(snackdrop)
                    
                    rungame()
                    banner = pygame.draw.rect(window, (0,0,0), (0,0,900,100))
                    pygame.display.update(banner)
                    menu = False

                if ExitButton.isOver(pos):
                    menu = False
                    pygame.quit()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Main Run

mainmenu()