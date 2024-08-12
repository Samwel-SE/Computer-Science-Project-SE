# imports script I wrote for procedural generation
import perlinnoise
import sys
import pygame
from pygame.locals import QUIT

import random


# game object class, to be inherited by player and projectile class
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

    def __init__(self, screen_width, screen_height, smoothness, colour):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.smoothness = smoothness
        self.colour = colour
        self.y = perlinnoise.generate(self.screen_width, self.smoothness)
        self.map_pieces = []

        for x in range(0, self.screen_width):
            self.map_pieces.append([])
            for y in range(0, self.y[x]):
                self.map_pieces[x].append(
                    GameObject(x, self.screen_height - y, 1, 1, green)
                )

    def draw(self):
        for x in self.map_pieces:
            for y in range(len(x)):
                x[y].draw()


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
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if pygame.mouse.get_pressed(3) and len(self.bombs) == 0:
        #         self.bombs.append(
        #             Bomb(
        #                 self.x + 2,
        #                 self.y + 2,
        #                 3,
        #                 3,
        #                 (255, 255, 0),
        #                 self.bomb_dx,
        #                 self.bomb_dy,
        #             )
        #         )

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
            output_tuple[0] = self.x + (cursor_tuple[0] - self.x) * 0.08
            self.bomb_dx = output_tuple[0] - self.x
        else:
            output_tuple[0] = self.x - (self.x - cursor_tuple[0]) * 0.08
            self.bomb_dx = output_tuple[0] - self.x
        if cursor_tuple[1] <= (self.y + 2):
            output_tuple[1] = self.y - (self.y - cursor_tuple[1]) * 0.08
            self.bomb_dy = output_tuple[1] - self.y
        else:
            output_tuple[1] = self.y + (cursor_tuple[1] - self.y) * 0.08
            self.bomb_dy = output_tuple[1] - self.y
        return output_tuple


# colours
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
green = (0, 100, 10)
# pygame initialisation
pygame.init()
DISPLAYSURF = pygame.display.set_mode((600, 600))
DISPLAYSURF.fill(black)


Clock = pygame.time.Clock()
pygame.display.set_caption("Bomber Bros")

terr = Map(
    DISPLAYSURF.get_width(),
    DISPLAYSURF.get_height(),
    random.randint(40, 70),
    green,
)


player1 = Player(100, 100, 5, 5, red)

# game loop
while True:
    DISPLAYSURF.fill(black)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        player1.inputs()

    player1.jump()
    if player1.movement[0]:
        player1.x += 3
    if player1.movement[1]:
        player1.x -= 3

    # game objects drawn here
    terr.draw()
    player1.draw()
    pygame.display.flip()
    Clock.tick(60)
