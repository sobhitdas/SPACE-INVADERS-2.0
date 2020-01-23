import pygame
import random
import math
from pygame import mixer


pygame.init()  # Intialize the pygame

screen = pygame.display.set_mode((800, 600))  # Create the screen

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)  #To play it on a loop


# Title and icon
pygame.display.set_caption("Space Invaders 2.0")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg =[]
enemyX =[]
enemyY =[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6

#Multiple enemies

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735)) # To make enemy appear at random places
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 3
bulletY_change = 10
bullet_state = "ready"  # You can't see the bullet on the screen #Fire-The bullet is currently moving

#Score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10

#Game Over Text
over_font=pygame.font.Font('freesansbold.ttf',64)

def show_score(x,y):
    score = font.render("SCORE :"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,0,0))
    screen.blit(over_text,(200,250))


def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means to draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # blit means to draw


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False



# Game loop
running = True
while running:

    screen.fill((0, 0, 0))  # red,green,blue(rgb) #Background solid color

    # Adding background image

    background = pygame.image.load('background.png')
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # To close the window when user quits the program
            running = False

        # IF Keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if bullet_state is"ready":
                     bullet_Sound = mixer.Sound('laser.wav')
                     bullet_Sound.play()
                    #get the current x-coordinate of the spaceship
                     bulletX = playerX
                     fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # giving boundaries to our spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy Movement
    for i in range(num_of_enemies):

        #Game over
        if enemyY[i] >440:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i]<= 0:
            enemyX_change[i] = 5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i]>= 736:
            enemyX_change[i] = -5
            enemyY[i] += enemyY_change[i]


        #Collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            bullet_Sound = mixer.Sound('explosion.wav')
            bullet_Sound.play()
            bulletY=480
            bullet_state = "ready"
            score_value+=1
            enemyX[i]= random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)


    # bullet movement

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(playerX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)  # To call the function for drawing the player
    show_score(textX,textY)
    pygame.display.update()  # To update the window every time an event is changed
