#importing random for grnrating random number for pipe pos
import random

#importing sys to close the game on window closing
import sys

#importing pygame
import pygame
from pygame.locals import *

#importing date time
import datetime

#Global Variable
FPS = 60
LEVEL =1
i=1
SCREENWIDTH = 1080
SCREENHEIGHT = 720
points = 0
#fetching the highscore from the text file
with open("score.txt", "r") as f:
    score_ints = [int(x) for x in f.read().split()]
    highscore = max(score_ints)
#other variables
game_speed = -4
death_count = 0

#setting screen width
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUND = SCREENHEIGHT * 0.8

#game object holders
GAME_SPRITES =  {}
GAME_SOUND ={}

#game object paths
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background1.jpg'
PIPE = 'gallery/sprites/pipe.png'

#welcome screen deffination
def welcomeScreen():
    #shows welcome image on screen

    #defines the bird position by x and y co ordinates
    birdposx = int(SCREENWIDTH/5)
    birdposy = int((SCREENHEIGHT - GAME_SPRITES['bird'].get_height())/2)

    #defines the score position
    messageposx = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messageposy = int(SCREENHEIGHT*0.13)

    #defines base position
    baseposx = 0


    while True:
        for event in pygame.event.get():
            #if clickis on close button or escape button close the game
            if event.type ==QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #if user press space key to flapp or jump
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                #blitting all the images or game objects
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['bird'], (birdposx,birdposy))
                SCREEN.blit(GAME_SPRITES['message'], (messageposx,messageposy))
                SCREEN.blit(GAME_SPRITES['base'], (baseposx,GROUND))

                #updateing the display using py game
                pygame.display.update()
                #locking the fps
                FPSCLOCK.tick(FPS)


#main game funtion defination
def mainGame():
    #from start it fetches the background(1) and blit it
    BACKGROUND = f'gallery/sprites/background1.jpg'
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    SCREEN.blit(GAME_SPRITES['background'], (0, 0))

    #initialising bird position using x and y co ordinates
    birdposx = int(SCREENWIDTH / 5)
    birdposy = int(SCREENWIDTH / 2)

    #base postions
    baseposx = 0

    # Creating 4 pipes for blitting on the screen with random gap between upper pipe and lower pipe uning "getRandomPipe" function
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()
    newPipe4 = getRandomPipe()


    # at first Adding 4 piepes then we will move them to the left
    # if any pipe reaches the left edge we will add anathoier pipe at the right edge so the flow of pipe will continue

    # List of upper pipes postion for the starting 4
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 450, 'y': newPipe2[0]['y']},
        {'x': SCREENWIDTH + 700, 'y': newPipe3[0]['y']},
        {'x': SCREENWIDTH + 950, 'y': newPipe4[0]['y']},
    ]
    #List of lower pipes for fist 4 pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 450, 'y': newPipe2[1]['y']},
        {'x': SCREENWIDTH + 750, 'y': newPipe3[1]['y']},
        {'x': SCREENWIDTH + 950, 'y': newPipe4[1]['y']},

    ]

    #matching the pipe velocity with the game speed so that the speed increases if game speed increases
    pipeVelX = game_speed

    #bird property initialisation
    birdVelY = -9
    birdMAxVelY = 10
    birdMinVelY = -8
    birdAccY = 1

    birdFlapAccv = -8  #velocity during flppying

    birdFlapped = False  #WHEN space is not pressed

    while True:
        #collect the events if any key is pressed or not
        for event in pygame.event.get():
            #closes the game if close button or excape button pressed
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if key up or space pressed it increases the height of bird and play a flapping sound
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if birdposy > 0:
                    #increase the height
                    birdVelY = birdFlapAccv
                    #upadtes the values
                    birdFlapped = True
                   # play the flapping sound
                    GAME_SOUND['wing'].play()


        #checking for colision using iscollide function
        crashTest = isCollide(birdposx, birdposy, upperPipes,
                              lowerPipes)  # This function will return true if the bird is crashed
        if crashTest:
            return

        #initializing and updating birdMidpos for further use
        birdMidPos = birdposx + GAME_SPRITES['bird'].get_width() / 2

        for pipe in upperPipes:

            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2

            #scoring condition
            #if the bird flies though the middle gap of the upper pipe and lower pipe score increass
            if pipeMidPos <= birdMidPos < pipeMidPos + 5:
                pipeVelX = game_speed
                #calling scoring funtion to update the score and other veriable for level or speed
                scoring()
                #playing a point sound
                GAME_SOUND['point'].play()


        #increasing falling gap/speed
        if birdVelY < birdMAxVelY and not birdFlapped:
            birdVelY += birdAccY

        #updates the bird hieight if birdFlapped is true and update it as false
        if birdFlapped:
            birdFlapped = False
        birdH = GAME_SPRITES['bird'].get_height()
        birdposy = birdposy + min(birdVelY, GROUND - birdposy - birdH)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # blit the background,pipes, base and bird
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))


        SCREEN.blit(GAME_SPRITES['base'], (baseposx, GROUND))
        SCREEN.blit(GAME_SPRITES['bird'], (birdposx, birdposy))
        ############################################
        #displaying the score geitting the numbers avilabe in the points

        myDigits = [int(x) for x in list(str(points))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2
        #bliting the numbers (game objects)
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        ##################################################################
        #displaying the high score
        # same as the score displaying
        myDigits = [int(x) for x in list(str(highscore))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2 + 450

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        #updates the screen
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#defination for iscollide function to check if it colides with pipes or ground
def isCollide(birdposx,birdposy, upperPipes, lowerPipes):
    #check if the bird touches the skylimit or ground
    if birdposy > GROUND - 25 or birdposy < 0:
        GAME_SOUND['hit'].play()
        return True
    #CHECK if bird touches the upper pipes or not
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (birdposy < pipeHeight + pipe['y'] and abs(birdposx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND['hit'].play()
            return True

    # CHECK if bird touches the lower pipes or not
    for pipe in lowerPipes:
        if (birdposy + GAME_SPRITES['bird'].get_height() > pipe['y']) and abs(birdposx - pipe['x']) < \
                GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUND['hit'].play()
            return True

#if not collided in anyother it returns false
    return False


def getRandomPipe():
    #geenerating positions of pipe
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    #fixed value(gap) between two pipes
    offset = SCREENHEIGHT / 3

    #fixed value(gap) + random gap between two pipes
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = (SCREENWIDTH + 10)
    y1 = pipeHeight - y2 + offset
    #making the list of two pipes position
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    #retruning the list
    return pipe

#defining the scoring system
#INCREASE SCORE AND GAME SPEED
def scoring():

    global points, highscore, game_speed, FPS, LEVEL,i, BACKGROUND
    #wheneevr the function is called the score increase
    points += 1
    #plays a sound
    GAME_SOUND['point'].play()
    if points % 5 == 0:
          #per 2 point increase the game speed increase
          FPS = FPS +10
          #game_speed=game_speed-1
    if points % 5 == 0:
        # per 2 point increase the level increase
         LEVEL = LEVEL+1
         i = i + 1
        #changing the background based on the value of "i" between 1 to 3
         if(i<=3):

             BACKGROUND = f'gallery/sprites/background{i}.jpg'
             GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
             SCREEN.blit(GAME_SPRITES['background'], (0, 0))
         if (i > 3):
             i= 1
             BACKGROUND = 'gallery/sprites/background1.jpg'
             GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
             SCREEN.blit(GAME_SPRITES['background'], (0, 0))
    #update the screen and bliting
    pygame.display.update()




   #string and retriving the high score from the score.txt file
    with open("score.txt", "r") as f:
        #read the highscore
        score_ints = [int(x) for x in f.read().split()]
        highscore = max(score_ints)
        #if the current score is getter than the current highscore
        if points > highscore:
            highscore = points
            f = open("score.txt", "a")
            #writes the highscore
            f.write(str(highscore) + "\n")
            f.close()
        print(f"the high score is : {highscore}")



if __name__ == '__main__':
    #main function

    #initializing all pygame modules
    pygame.init()

    FPSCLOCK = pygame.time.Clock()

    #window name or caption
    pygame.display.set_caption('Flappy Bird by Arindam Sarkar')

    #game objects / sprites fetching
    GAME_SPRITES['numbers'] = (pygame.image.load('gallery/sprites/0.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/1.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/2.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/3.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/4.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/5.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/6.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/7.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/8.png').convert_alpha(),
                               pygame.image.load('gallery/sprites/9.png').convert_alpha(),
                               )


    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base1.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
                            pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
                            pygame.image.load(PIPE).convert_alpha()
                            )
    GAME_SPRITES['background']= pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['bird'] = pygame.image.load(PLAYER).convert_alpha()

    #Game sound
    GAME_SOUND['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUND['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUND['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')


    #game loop
    while True:
        #welcome screen
        welcomeScreen()
        #initializing variables that will be re-initialised when game starts over
        game_speed = -4
        points = 0
        FPS = 60
        #main game function
        mainGame()







