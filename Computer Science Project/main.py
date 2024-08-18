import random
import sys
import math

import pygame
from pygame.locals import QUIT


# imports script I wrote for procedural generation
import perlinnoise


# game object class, to be inherited by all other classes, apart from player cursor which uses pygame line function
class GameObject:

    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    def draw(self):
        pygame.draw.rect(
            DISPLAYSURF,
            self.colour,
            pygame.Rect(self.x, self.y, self.width, self.height),
        )

    def collision(self, obj2):
        if (self.x < obj2.x + obj2.width and self.x + self.width > obj2.x) and (
            self.y + self.height > obj2.y and self.y < obj2.y + obj2.height
        ):
            return True


# map class
class Map:

    def __init__(self, screen_width, smoothness, colour):
        self.screen_width = screen_width + 100
        self.smoothness = smoothness
        self.colour = colour
        self.y = perlinnoise.generate(self.screen_width, self.smoothness)
        self.map_pieces = []
        self.piece_width = 700

        for i in range(self.screen_width):
            self.map_pieces.append(
                GameObject(i, self.y[i], 1, self.piece_width, self.colour)
            )

    def draw(self):
        for i in range(self.screen_width):
            self.map_pieces[i].draw()

    def terrain_damgage(self, bomb):
        if b.exp_collision(self.map_pieces[bomb.x]):
            self.map_pieces[bomb.x].y += b.exp_rad
            for i in range(1, bomb.exp_rad):
                if b.exp_collision(self.map_pieces[bomb.x + i]):
                    self.map_pieces[bomb.x + i].y = math.sqrt(b.exp_rad**2 - (i)**2) + (self.map_pieces[bomb.x].y -49)
                if b.exp_collision(self.map_pieces[bomb.x - i]):
                    self.map_pieces[bomb.x - i].y = math.sqrt(b.exp_rad**2 - (i)**2) + (self.map_pieces[bomb.x].y -49)


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

    # adds the player cursor to the player draw function
    def draw(self):
        super().draw()

        # draws players cursor
        pygame.draw.line(
            DISPLAYSURF,
            red,
            (self.x + 2, self.y + 2),
            self.get_cursor(pygame.mouse.get_pos()),
            1,
        )

    # gets keys currently pressed so player character can move
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

        # Once the left mouse button is pressed and there are no other bombs on screen will create a bomb object,
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3) and len(self.bombs) == 0:
                self.bombs.append(
                    Bomb(
                        self.x + 2,
                        self.y + 2,
                        3,
                        3,
                        (255, 255, 0),
                        self.bomb_dx,
                        self.bomb_dy,
                    )
                )

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
        output_tuple = [0, 0]
        if cursor_tuple[0] >= (self.x + 2):
            output_tuple[0] = self.x + (cursor_tuple[0] - self.x) * 0.08 * 0.5
            self.bomb_dx = output_tuple[0] - self.x
        else:
            output_tuple[0] = self.x - (self.x - cursor_tuple[0]) * 0.08 * 0.5
            self.bomb_dx = output_tuple[0] - self.x
        if cursor_tuple[1] <= (self.y + 2):
            output_tuple[1] = self.y - (self.y - cursor_tuple[1]) * 0.08 * 0.5
            self.bomb_dy = output_tuple[1] - self.y
        else:
            output_tuple[1] = self.y + (cursor_tuple[1] - self.y) * 0.08 * 0.5
            self.bomb_dy = output_tuple[1] - self.y
        return output_tuple


# Bomb class
class Bomb(GameObject):

    def __init__(self, x, y, width, height, color, dx, dy):
        super().__init__(x, y, width, height, color)
        self.dx = round(dx)
        self.dy = round(dy)
        self.exp_rad = 50

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += 1

    # on collision with terrain bomb will explode calling explode function, explosion can damage player and and destroy terrain.
    def explode(self):
        pygame.draw.circle(
            DISPLAYSURF, (255, 155, 0), (self.x + 1, self.y + 1), self.exp_rad
        )

    # exp_collision function if for collisions between the circler explosion and other objects
    def exp_collision(self, obj2):
        if (self.x - obj2.x) ** 2 + (self.y - obj2.y) ** 2 <= self.exp_rad**2:
            return True


# colours
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

# creates procedurally generated terrain, parameters are: screen width and smoothness of terrain
terr = Map(DISPLAYSURF.get_width(), random.randint(35, 60), green)
# line below for testing explosions
# terr = Map(DISPLAYSURF.get_width(), 100, green)

# game objects: parameters are, in order (x, y, width, height, colour)
l_wall = GameObject(-99, 0, 100, 1000, blue)
r_wall = GameObject(DISPLAYSURF.get_width(), 0, 100, 1000, blue)

# player object
player1 = Player(300, 300, 5, 5, red)

Clock = pygame.time.Clock()
pygame.display.set_caption("Bomber Bros")

# stops player from seeing mouse cursor
pygame.mouse.set_visible(False)

# update loop ------------------------------------------------------------------------------------------------->
while True:

    # fills the screen black again so sprties actually move
    DISPLAYSURF.fill(black)

    # gets key preses and button presses
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
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
    if player1.collision(terr.map_pieces[player1.x]):
        player1.y = terr.map_pieces[player1.x].y - 5
        player1.jumping = False
        player1.jump_vel = player1.jump_height
    elif player1.collision(terr.map_pieces[player1.x + player1.width]):
        player1.y = terr.map_pieces[player1.x + player1.width].y - 5
        player1.jumping = False
        player1.jump_vel = player1.jump_height

    # bomb movement
    for i in player1.bombs:
        i.move()

    # game objects drawn here
    terr.draw()
    player1.draw()

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
            b.explode()
            terr.terrain_damgage(b)
            player1.bombs.pop()

    pygame.display.flip()
    Clock.tick(60)
