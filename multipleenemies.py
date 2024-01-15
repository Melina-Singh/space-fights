import pygame
import random
import math

from pygame import mixer 


# Initializing pyhame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800,600)) #800 is weidth and 700 is height
# print(screen)
# Bg
background = pygame.image.load("background.jpg")

# bg Sound 
mixer.music.load('background.mp3')
mixer.music.play(-1)

# Title of my game and ICOn
pygame.display.set_caption("Space Fights")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)


# Player 
playerimg = pygame.image.load('player.png')
playerX = 500
playerY = 505
playerX_change = 0


# Enemy
enemyimg =[]
enemyX =[]
enemyY =[]
enemyX_change =[]
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('devil.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50, 250))
    enemyX_change.append(0.2)
    enemyY_change.append(40)


# Bullets 
# Ready - we cant see the bullet on the screen
# fire - means The bullet is moving 
Bulletimg = pygame.image.load('bullets.png')
BulletX = 0
BulletY = 480
BulletX_change = 0.3
BulletY_change = 1
Bullet_state  = 'ready'

# score = 0
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def gameover_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x,y))

def fire_Bullet(x,y):
    global Bullet_state
    Bullet_state = 'fire'
    screen.blit(Bulletimg, (x + 16,y + 10)) #so that bullet appear in between 

def isCollision(enemyX,enemyY,BulletX,BulletY):
    distance = math.sqrt((math.pow(enemyX - BulletX, 2)) + (math.pow(enemyY - BulletY , 2)))
    if distance < 27:
        return True
    else:
        return False

# game Loop
running = True
# clock = pygame.time.Clock()

while running:

#  RGB Values are placed
    screen .fill((0, 0, 0))
    # background image
    screen.blit(background,(0,0))

    # playerX += 0.1  #this is for right hand movement
    # playerY += 0.1 thisis for down movement
    # playerX -= 0.1 thisis for left hand side movement
    # print(playerX)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
            # now lets start with the keyboard to check if the key strock is pressed 
            # so here the value is given to move the arrow key 0.1 left and right
        if event.type == pygame.KEYDOWN:
            # print("A keystroke is Pressed")
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if Bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # get the current x coordinate of the spaceship 
                    BulletX = playerX
                    fire_Bullet(BulletX , BulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0




# checking the boundaries od the spaceship so that it doesnt go out of the boarder
    playerX += playerX_change

    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX =736
    
# enemy Movement
    for i in range (num_of_enemies):

        # GameOver
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameover_text(200, 250)
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] =-0.3
            enemyY[i] += enemyY_change[i]

        # Collission
        collision = isCollision(enemyX[i], enemyY[i], BulletX, BulletY)
        if collision:
            BulletY = 480
            Bullet_state = 'ready'
            score_value += 1
            # print(score)
            enemyX[i] = random.randint(0,800)
            enemyY[i] = random.randint(50, 250)

            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()

        enemy(enemyX[i],enemyY[i], i)

# Bulleet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_state = 'ready'
        
    if Bullet_state is 'fire': 
        fire_Bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    
    
    player(playerX, playerY)

    show_score(textX, textY)
    
    pygame.display.update()
    # clock.tick(60)
