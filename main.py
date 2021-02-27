import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the sceen
screen = pygame.display.set_mode((800,600))

# Background image
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav.mpeg')
mixer.music.play(-1)

# caption and icon
pygame.display.set_caption("BOUNCING BALL")
icon = pygame.image.load('bhaalu.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#bhoot

bhootImg = []
bhootX = []
bhootY = []
bhootX_change = []
bhootY_change = []
no_of_bhoot = 6

for i in range(no_of_bhoot):

  bhootImg.append(pygame.image.load('bhoot.png'))
  bhootX.append(random.randint(0,735))
  bhootY.append(random.randint(50,200))
  bhootX_change.append(2.0)
  bhootY_change.append(40)

#goli
# ready - cant see the goli on the screen
# fire - goli is currently moving
goliImg = pygame.image.load('goli.png')
goliX = 0
goliY = 480
goliX_change = 0
goliY_change = 10
goli_state = "ready"

# score
score_value = 0
font = pygame.font.Font('Twinkle Dream.ttf', 30)

textX = 10
textY = 10

# game over
over_font = pygame.font.Font('Twinkle Dream.ttf', 64)

def showScore(x,y):
  score = font.render("score :" + str(score_value), True, (255,255,255))
  screen.blit(score, (x, y))

def game_over_text():
  over_text = over_font.render("GAME OVER", True, (255,255,255))
  screen.blit(over_text, (200, 250))


def player(x,y):
  screen.blit(playerImg, (x, y))

def bhoot(x,y, i):
  screen.blit(bhootImg[i], (x, y))

def goli_shooted(x,y):
  global goli_state
  goli_state = "fire"
  screen.blit(goliImg, (x + 16, y + 10))

def iscollision(bhootX, bhootY, goliX, goliY,):
  distance = math.sqrt((math.pow(bhootX-goliX, 2))+ (math.pow(bhootY-goliY,2)))
  if distance < 27:
    return True
  else:
    return False  

# game loop
running = True
while running:
  
  # RGB - red, green, blue
  screen.fill((0, 0, 0))
 
  # Background image
  screen.blit(background,(0,0))
   

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

     #if keystroke is pressed check weather its right or left
    if event.type == pygame.KEYDOWN:
      print("A keystroke is pressed")
      if event.key == pygame.K_LEFT:
        playerX_change = -7.0
      if event.key == pygame.K_RIGHT:
        playerX_change = 7.0
      if event.key == pygame.K_SPACE:
        if goli_state is "ready":
          goli_sound = mixer.Sound('gaana.wav')
          goli_sound.play()
          goliX = playerX
          goli_shooted(goliX, goliY)

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        playerX_change = 0    

  # 5 = 5 + 0.1 -> 5 = 5 - 0.1
  # 5 = 5 + 0.1

  # checking boundary of udn_tastari
  playerX += playerX_change
  
  if playerX <= 0:
    playerX = 0 
  elif playerX >= 736:
    playerX = 736  
  
  # bhoot ka moment
  for i in range(no_of_bhoot):

    # game over
    if bhootY[i] > 450:
      for j in range(no_of_bhoot):
        bhootY[j] = 2000
      game_over_text()
      break  

    bhootX[i] += bhootX_change[i]
    if bhootX[i] <= 0:
      bhootX_change[i] = 2.0
      bhootY[i] += bhootY_change[i]
    elif bhootX[i] >= 736:
      bhootX_change[i] = -2.0 
      bhootY[i] += bhootY_change[i]

    # collision
    collision = iscollision(bhootX[i],bhootY[i],goliX,goliY)
    if collision:
      fatne_ka_sound = mixer.Sound('yoboy.wav')
      fatne_ka_sound.play()
      goliY = 480
      goli_state = "ready"   
      score_value += 1
      bhootX[i] = random.randint(0,735)
      bhootY[i] = random.randint(50,200)

    bhoot(bhootX[i], bhootY[i], i)
   
  # goli ka moment 
  if goliY <= 0:
    goliY = 480 
    goli_state = "ready"

  if goli_state is "fire":
    goli_shooted(goliX, goliY)
    goliY -= goliY_change 


  player(playerX, playerY)
  showScore(textX, textY)
  pygame.display.update()