import random
import sys

import pygame
from pygame.locals import QUIT

#imports script I wrote for procedurally generation
import perlinnoise

#game object class, to be inherited by player and projectile class
class GameObject():

  def __init__(self, x, y, width, height, colour):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.colour = colour

  def draw(self):
    pygame.draw.rect(DISPLAYSURF, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))

  def collision(self, obj2):
    if (self.x < obj2.x + obj2.width and self.x + self.width > obj2.x) and (self.y + self.height > obj2.y and self.y < obj2.y + obj2.height):
      return True

#map class
class Map():

  def __init__(self, screen_width, smoothness, colour):
    self.screen_width = screen_width
    self.smoothness = smoothness
    self.colour = colour
    self.y = perlinnoise.generate(self.screen_width, self.smoothness)
    self.map_pieces = []

    for i in range(1600):
      self.map_pieces.append(GameObject(i, self.y[i], 1, 700, self.colour))

  def draw(self):
    for i in range(1600):
      self.map_pieces[i].draw()



#player class inherits gameobject class
class Player(GameObject):                         

  def __init__(self, x, y, width, height, colour):
    super().__init__(x, y, width, height, colour)
    self.movement = [False, False]
    self.jumping = False
    self.jump_vel = 12
    self.jump_height = self.jump_vel

  #gets keys currently pressed so player character can move
  def inputs(self):                                         
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_d:
        self.movement[0] = True
      if event.key == pygame.K_a:
        self.movement[1] = True
      if event.key == pygame.K_w and self.jumping == False:
        self.jumping = True
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_d:
          self.movement[0] = False
        if event.key == pygame.K_a:
          self.movement[1] = False

  #player jump
  def jump(self):
    if self.jumping:
      self.y -= self.jump_vel
      self.jump_vel -= 1  

      #jump_vel goes from positive to negative during jump function allowing player to fall back down to the ground.
      #the below statement ends the jump function once jump vel has become smaller than negative jump height
      if self.jump_vel < -self.jump_height:
        self.jumping = False
        self.jump_vel = self.jump_height

    #while player has not pressed jump key they will constantly move downwards as to not break game
    else:
      self.y += 10


#pygame initialisation
pygame.init()                                            
background = (255, 255, 255)
DISPLAYSURF = pygame.display.set_mode((1500, 800))
DISPLAYSURF.fill(background)                                                              

#colours 
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

#creates procedurally generated terrain, parameters are: screen width and smoothness of terrain
terr = Map(1600, random.randint(140, 170), black)  

#game objects
l_wall = GameObject(0, 0, 1, 800, blue)
r_wall = GameObject(1495, 0, 1, 800, blue)
player1 = Player(300, 300, 5, 5, red,)

Clock = pygame.time.Clock()
pygame.display.set_caption('Bomber Bros')      

#game loop
while True:                                                                 
  DISPLAYSURF.fill(background)   
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    player1.inputs()

  #player movement
  player1.jump()
  if player1.movement[0]:                                                  
    player1.x += 3
  if player1.movement[1]:
    player1.x -= 3

  #player collision with ground: checks if any pixels making up bottom of player square overlapping with ground
  for i in range(0,4):
    if player1.collision(terr.map_pieces[player1.x +i]):
      player1.y = terr.map_pieces[player1.x].y - 5
      break
  
  #player collision with game boundaries
  if player1.collision(l_wall):
    player1.x = 5
  elif player1.collision(r_wall):
    player1.x = 1490


  #game objects drawn here
  terr.draw()
  player1.draw()
  pygame.display.update()
  Clock.tick(60)  