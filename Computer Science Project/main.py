import random
import sys
import math

import pygame
from pygame.locals import QUIT


# imports 1d Perlin Noise generation script I wrote to generate the maps
import perlinnoise


# game object class, to be inherited by all other classes
class GameObject:

    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))

    def collision(self, obj2):
        if (self.x < obj2.x + obj2.width and self.x + self.width > obj2.x) and (
            self.y + self.height > obj2.y and self.y < obj2.y + obj2.height
        ):
            return True


# Map class
class Map:

    def __init__(self, screen_width, colour):
        self.screen_width = screen_width + 100
        self.colour = colour
        self.map_pieces = []
        self.piece_width = 700

    # uses perlin noise script to generate the map
    def generate_map(self):
        self.map_pieces.clear()
        y_vars = perlinnoise.generate(self.screen_width, random.randint(30, 40))
        # y_vars = perlinnoise.generate(self.screen_width, 100)  <--- Used for testing certain bombs on flat terrain
        
        for i in range(self.screen_width):
            self.map_pieces.append(GameObject(i, y_vars[i], 1, self.piece_width, self.colour))

    # iterates through and draws all the gameobjects making up the map
    def draw(self):
        for i in range(self.screen_width):
            self.map_pieces[i].draw()

    def terrain_damgage(self, bomb):
        self.map_pieces[bomb.x].y += bomb.exp_rad
        for i in range(1, bomb.exp_rad):
            if self.map_pieces[bomb.x +i].y > math.sqrt(bomb.exp_rad**2 - (i)**2) + (self.map_pieces[bomb.x].y -49):
                break
            if bomb.exp_collision(self.map_pieces[bomb.x + i]):
                self.map_pieces[bomb.x + i].y = math.sqrt(bomb.exp_rad**2 - (i)**2) + (self.map_pieces[bomb.x].y -49)
            if bomb.exp_collision(self.map_pieces[bomb.x - i]):
                self.map_pieces[bomb.x - i].y = math.sqrt(bomb.exp_rad**2 - (i)**2) + (self.map_pieces[bomb.x].y -49)


# player class inherits gameobject class
class Player(GameObject):

    def __init__(self, x, y, width, height, colour):
        super().__init__(x, y, width, height, colour)

        # movement tuple's bool's change when a and d keys pressed, if true the player will move left or right
        self.movement = [False, False]

        # jumping is true when player is not touching the ground
        self.jumping = False
        self.jump_vel = 12
        self.jump_height = 12

        # bombs object array
        self.bombs = []
        # bullet direction x and y
        self.bomb_dx = 0
        self.bomb_dy = 0

        # player life count
        self.lives = 3

        # current weapon
        self.weapons = ["Bounce", "Splinter", "Guided"]
        self.current_weapon = 0

    # adds drawing player cursor, life count and currently equipped weapon
    def draw(self):
        super().draw()

        # draws players cursor
        pygame.draw.line(DISPLAYSURF, self.colour, (self.x + 2, self.y + 2), self.get_cursor(pygame.mouse.get_pos()),1)

        #draws player live count
        for i in range(self.lives):
            pygame.draw.rect(DISPLAYSURF, self.colour, pygame.Rect(i*10, 0, 5, 10))

        # shows currently equipped weapon at the top of the screen
        if self.current_weapon > 2:
            self.current_weapon = 0
        DISPLAYSURF.blit(the_font.render(self.weapons[self.current_weapon], False, red), (40, 0))

    # gets keys currently pressed so player character can move
    def inputs(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.movement[0] = True
            if event.key == pygame.K_a:
                self.movement[1] = True
            if event.key == pygame.K_w and self.jumping == False:
                self.jumping = True

            # to swap through weapon list
            if event.key == pygame.K_e:
                self.current_weapon += 1
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.movement[0] = False
            if event.key == pygame.K_a:
                self.movement[1] = False

        # Once the left mouse button is pressed and there are no other bombs on screen will create a bomb object,
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3) and len(self.bombs) == 0:
                self.bombs.append(Bomb(self.x + 2, self.y + 2, 3, 3, (255, 255, 0), self.bomb_dx, self.bomb_dy))

    # player jump
    def jump(self):
        if self.jumping:
            # jump_vel goes from positive to negative during jump function allowing player to fall back down to the ground.
            self.y -= self.jump_vel
            self.jump_vel -= 1

        # while player has not pressed jump key they will constantly move downwards as to not break game
        else:
            self.y += 5

    # gets coordinates of line making up player cursor
    def get_cursor(self, cursor_tuple):
        # diff dict stores the difference in x & y between cursor pos and mouse pos
        diff = {"x": abs(cursor_tuple[0] -self.x) *0.04, "y": abs(cursor_tuple[1] -self.y) *0.04}
        
        if cursor_tuple[0] >= (self.x + 2): 
           self.bomb_dx = diff["x"]
        else: 
            self.bomb_dx = -diff["x"]

        if cursor_tuple[1] <= (self.y + 2): 
            self.bomb_dy = -diff["y"]
        else: 
            self.bomb_dy = diff["y"]
        

        return [self.bomb_dx +self.x+2 , self.bomb_dy +self.y+2]


# Bomb class, inherits Game Object Class
class Bomb(GameObject):

    def __init__(self, x, y, width, height, colour, dx, dy):
        super().__init__(x, y, width, height, colour)
        self.dx = round(dx)
        self.dy = round(dy)
        self.exp_rad = 50
        self.bounces = 3

    # movement of the bomb
    def move(self):
        self.x += round(self.dx)
        self.y += round(self.dy)
        self.dy += 1
    
    # bounce function when bounces are greater than 0, dx and dy decrease to mimic how a ball would bounce
    def bounce(self):
        self.dx = self.dx * 0.7
        self.dy = -(self.dy) * 0.7
        self.bounces -= 1

    # draws the expxlosion of the bomb
    def explode(self):
        pygame.draw.circle(DISPLAYSURF, (255, 155, 0), (self.x + 1, self.y + 1), self.exp_rad)

    # checks whether points of other objects overlap with explosion, returning True or False
    def exp_collision(self, obj2):
        if ((self.x -1)- obj2.x) ** 2 + ((self.y +1) - obj2.y) ** 2 <= self.exp_rad**2:
            return True


# colours, represented by RGB colour codes stored as tuples
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
green = (0, 100, 10)

# pygame initialisation
pygame.init()

# surface object
DISPLAYSURF = pygame.display.set_mode((600, 800), pygame.FULLSCREEN)
DISPLAYSURF.fill(black)

# initialises the font to be used
pygame.font.init ()
the_font = pygame.font.SysFont("Arial", 10)


# terr is the map object
terr = Map(DISPLAYSURF.get_width(), green)

# the function below uses the 1d perlin noise generation script to create bumps and grooves in terrain
terr.generate_map()
# game objects: parameters are, in order (x, y, width, height, colour)
l_wall = GameObject(-99, 0, 100, 1000, blue)
r_wall = GameObject(DISPLAYSURF.get_width(), 0, 100, 1000, blue)

# player object
player1 = Player(300, 300, 5, 5, red)

Clock = pygame.time.Clock()
pygame.display.set_caption("Bomber Bros")

# stops player from seeing mouse cursor
pygame.mouse.set_visible(False)

# count down is used to count down seconds after player death till player respawn
count_down = pygame.event.custom_type()
pygame.time.set_timer(count_down, 1000)

# pause to allow game to begin countdown upon player death
pause = False
counter = 3 #counter for seconds on the timer

# text displayed in the middle of the screen upon round and game end
text = ""

# update loop ---------------------------------------------------------------------------------------------------------------------------------->
while True:
    # fills the screen black again so sprties actually move
    DISPLAYSURF.fill(black)

    # gets key preses and button presses
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        # checks if pause is enabled, if it is a 3 second count down begins
        if pause and event.type == count_down:
            counter -= 1 
            text = "Blue Wins. Next Round Begins " + str(counter)
            player1.movement = [False, False]

            # once the countdown ends following code is ran
            if counter == 0:    
                pygame.time.set_timer(pygame.USEREVENT, 1)
                pause, text = False, ""
                player1.x, player1.y, player1.colour, = 300, 300, red, 
                counter = 3
                terr.generate_map()
                
        # disables player inputs whilst the countdown is happening        
        if not(pause):
            player1.inputs()

    # below is code that prevents player from moving when certain parts of the terrain are too high for the player to traverse without jumping
    if terr.map_pieces[player1.x + 8].y < player1.y - 3:
        player1.movement[0] = False
    if terr.map_pieces[player1.x - 3].y < player1.y - 3:
        player1.movement[1] = False

    # player movement
    player1.jump()
    if player1.movement[0]:
        player1.x += 3
    if player1.movement[1]:
        player1.x -= 3

    # player collision with game boundaries
    if player1.collision(l_wall):
        player1.x = 3
    elif player1.collision(r_wall):
        player1.x = DISPLAYSURF.get_width() - 9

    # player collision with ground: checks if any bottom corner pixels player overlapping with terrain
    if player1.collision(terr.map_pieces[player1.x]) or player1.collision(terr.map_pieces[player1.x + player1.width]):
        player1.y = terr.map_pieces[player1.x].y - 5
        player1.jumping = False
        player1.jump_vel = player1.jump_height

    # bomb movement
    for i in player1.bombs:
        i.move()

    # game objects drawn here
    terr.draw()
    player1.draw()

    # draws text
    DISPLAYSURF.blit(the_font.render(text, False, blue), (400, 250))

    # walls can be drawn for testing collision
    # r_wall.draw()
    # l_wall.draw()

    # draws bombs once the player has pressed the mouse
    for b in player1.bombs:
        b.draw()
        # checks for collision between bombs with walls and terrain
        if b.collision(r_wall) or b.collision(l_wall):
            b.explode()
            player1.bombs.pop()

        elif b.collision(terr.map_pieces[round(b.x)]):
            if b.bounces > 0:
                b.bounce()
            else:
                b.explode()
                player1.bombs.pop()
                terr.terrain_damgage(b)
                if b.exp_collision(player1) or b.exp_collision(player1):
                    player1.lives -= 1
                    print(player1.lives)
                    pause, player1.colour, player1.x, player1.y, text = True, black, 300, -1000, "Blue Wins. Next Round Begins " + str(counter)
                
    pygame.display.update(pygame.Rect(0, 0, DISPLAYSURF.get_width(), 10))
    pygame.display.update(pygame.Rect(0, 10, DISPLAYSURF.get_width(), DISPLAYSURF.get_height()))
    Clock.tick(60)
