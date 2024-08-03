import random
import sys

import pygame
from pygame.locals import QUIT

import math

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
    
    #movement tuple's bool's change when a and d keys pressed, if true the player will move left or right
    self.movement = [False, False]
    
    #jumping is true when player is not touching the ground
    self.jumping = False
    self.jump_vel = 12
    self.jump_height = 12

    #bombs object array
    self.bombs = []
    #bullet direction x and y
    self.bomb_dx = 0
    self.bomb_dy = 0

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

    #Once the left mouse button is pressed and there are no other bombs on screen will create a bomb object, 
    if event.type == pygame.MOUSEBUTTONDOWN:
      if pygame.mouse.get_pressed(3) and len(self.bombs) == 0:
        self.bombs.append(Bomb(self.x+2, self.y+2, 3, 3, (255, 255, 0),self.bomb_dx, self.bomb_dy))

  #player jump
  def jump(self):
    if self.jumping:
      
      #jump_vel goes from positive to negative during jump function allowing player to fall back down to the ground.
      self.y -= self.jump_vel
      self.jump_vel -= 1  
    
    #while player has not pressed jump key they will constantly move downwards as to not break game
    else:
      self.y += 5

  #gets coordinates of line making up player cursor
  def get_cursor(self, cursor_tuple):
    output_tuple = [0,0]
    if cursor_tuple[0] >= (self.x +2):
      output_tuple[0] = self.x +(cursor_tuple[0] -self.x)*0.08
      self.bomb_dx = output_tuple[0] - self.x
    else:
      output_tuple[0] = self.x -(self.x - cursor_tuple[0])*0.08
      self.bomb_dx = output_tuple[0] - self.x
    if cursor_tuple[1] <= (self.y +2):
      output_tuple[1] = self.y - (self.y - cursor_tuple[1])*0.08
      self.bomb_dy = output_tuple[1] - self.y
    else:
      output_tuple[1] = self.y +(cursor_tuple[1] - self.y)*0.08
      self.bomb_dy = output_tuple[1] - self.y
    return output_tuple

#Bomb class.
class Bomb(GameObject):

  def __init__(self, x, y, width, height, color, dx, dy):
    super().__init__(x, y, width, height, color)
    self.dx = dx
    self.dy = dy
    self.exp_rad = 49

  def move(self):  
    self.x += self.dx
    self.y += self.dy
    self.dy += 1
  
  #on collision with terrain bomb will explode calling explode function, explosion can damage player and and destroy terrain.
  def explode(self):
    pygame.draw.circle(DISPLAYSURF, (255, 165, 0), (self.x, self.y), self.exp_rad)

#colours 
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
green = (0, 100, 10)
#pygame initialisation
pygame.init()                                            
DISPLAYSURF = pygame.display.set_mode((1500, 800))
DISPLAYSURF.fill(black)                                                              



#creates procedurally generated terrain, parameters are: screen width and smoothness of terrain
terr = Map(1600, random.randint(140, 170), green)  

#game objects: parameters are, in order (x, y, width, height, colour)
l_wall = GameObject(-99, 0, 100, 1000, blue)
r_wall = GameObject(1495, 0, 100, 1000, blue)

#player object
player1 = Player(300, 300, 5, 5, red)

Clock = pygame.time.Clock()
pygame.display.set_caption('Bomber Bros')      


#game loop
while True:                                                                 
  DISPLAYSURF.fill(black)   
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    player1.inputs()

  if terr.map_pieces[player1.x + 8].y < player1.y - 3:
    player1.movement[0] = False
  if terr.map_pieces[player1.x  -3].y < player1.y  - 3:
    player1.movement[1] = False

  #player movement
  player1.jump()
  if player1.movement[0]:                                                  
    player1.x += 3
  if player1.movement[1]:
    player1.x -= 3

  #bomb movement
  for i in player1.bombs:
    i.move()

  #player collision with ground: checks if any pixels within width of player square overlapping with player
  for i in range(0,4):
    if player1.collision(terr.map_pieces[player1.x +i]):
      player1.y = terr.map_pieces[player1.x].y - 5
      player1.jumping = False
      player1.jump_vel = player1.jump_height
      break
      
  #player collision with game boundaries
  if player1.collision(l_wall):
    player1.x = 2
  elif player1.collision(r_wall):
    player1.x = 1490

  #game objects drawn here
  terr.draw()
  player1.draw()
  
  #draws bombs once the player has pressed the mouse
  for b in player1.bombs:
    b.draw()

    #checks for collision between bombs and terrain
    if b.collision(r_wall) or b.collision(l_wall) or b.collision(terr.map_pieces[round(b.x)]):
      b.explode()
      terr.map_pieces[round(b.x)].y += b.exp_rad*2
      for i in range(1, b.exp_rad*2):
        if b.exp_rad*2 < (i/3)**2 +math.sqrt(b.exp_rad):
          break
        terr.map_pieces[round(b.x) + i].y += b.exp_rad*2 - (i/3)**2 +math.sqrt(b.exp_rad*2)
        terr.map_pieces[round(b.x) - i].y += b.exp_rad*2 - (i/3)**2 +math.sqrt(b.exp_rad*2)
      player1.bombs.pop()
    


  #draws player1 cursor
  pygame.draw.line(DISPLAYSURF, red, (player1.x + 2, player1.y + 2), player1.get_cursor(pygame.mouse.get_pos()), 1)
  pygame.display.update()
  Clock.tick(60)  