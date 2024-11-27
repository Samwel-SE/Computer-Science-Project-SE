import random
import sys
import math

import pygame
from pygame.locals import QUIT

from network import Network

# imports 1d Perlin Noise generation script I wrote to generate the maps
import perlinnoise


# THIS SCRIPT IS COMPLETELY ORIGINAL ---------------------------------------------------------------------------------------------------------------------------------

# game object class, to be inherited by all other classes
class GameObject:

    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour

    # draws the gameobject 
    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))

    def collision(self, obj2):
        if (self.x < obj2.x + obj2.width and self.x + self.width > obj2.x) and (self.y + self.height > obj2.y and self.y < obj2.y + obj2.height):
            return True

    #gets object position
    def get_pos(self):
        return self.x, self.y
    
    #sets object position
    def set_pos(self, pos):
        self.x, self.y = pos[0], pos[1]


# Map class
class Map:

    def __init__(self, colour):
        self.screen_width = DISPLAYSURF.get_width()
        self.colour = colour
        self.map_pieces = []

        # stores y variables of all the objects making up the map
        self.y_vars = 0
        self.piece_length = 700

    # creates map obj
    def create_map_obj(self):
        self.map_pieces.clear()
        for i in range(self.screen_width):
            self.map_pieces.append(GameObject(i, self.y_vars[i], 1, self.piece_length, self.colour))



    # iterates through and draws all the gameobjects making up the map
    def draw(self):
        for i in range(self.screen_width):
            self.map_pieces[i].draw()



# player class inherits gameobject class
class Player(GameObject):
    
    def __init__(self, x, y, width, height, colour):
        super().__init__(x, y, width, height, colour)

        # movement tuple's bool's change when a and d keys pressed, if true the player will move left or right
        self.move_right = False
        self.move_left = False

        #cursor position
        self.cursor_pos = [0,0]

        # jumping is true when player is not touching the ground
        self.jumping = False
        self.jump_vel = 12
        self.jump_height = 12
        # bombs object array
        self.bombs = []
        self.bomb_init = 0
        # bullet direction x and y
        self.bomb_dx = 0
        self.bomb_dy = 0
        
        self.lives = 3

        # current weapon
        self.weapons = ["Bounce", "Splinter", "Guided"]
        self.current_weapon = 0


    # adds drawing player cursor, life count and currently equipped weapon
    def draw(self):
        super().draw()

        # draws players cursor
        pygame.draw.line(DISPLAYSURF, self.colour, (self.x + 2, self.y + 2), self.cursor_pos,1)

        #draws player live count
        for i in range(self.lives):
            pygame.draw.rect(DISPLAYSURF, self.colour, pygame.Rect(self.lives + i*10, 0, 5, 10))

        # shows currently equipped weapon at the top of the screen
        if self.current_weapon > 2:
            self.current_weapon = 0
        DISPLAYSURF.blit(the_font.render(self.weapons[self.current_weapon], False, self.colour), (self.lives, 0))


    # gets keys currently pressed so player character can move
    def inputs(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.move_right = True
            if event.key == pygame.K_a:
                self.move_left = True
            if event.key == pygame.K_w and self.jumping == False:
                self.jumping = True

            # to swap through weapon list
            if event.key == pygame.K_e:
                self.current_weapon += 1
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.move_right = False
            if event.key == pygame.K_a:
                self.move_left = False

        # Once the left mouse button is pressed and there are no other bombs on screen will create a bomb object,
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3) and len(self.bombs) == 0:
                self.bombs.append(Bomb(self.x + 2, self.y + 2, 3, 3, (255, 255, 0), self.bomb_dx, self.bomb_dy))
                self.bomb_init = 1

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
        
        self.cursor_pos = [self.bomb_dx +self.x+2 , self.bomb_dy +self.y+2]
        return self.cursor_pos

    # function is used to control the client player in host players game
    def set_pos(self, client_data):
        # coords 
        self.x = client_data[0]
        self.y = client_data[1]
        # cursor coords
        self.cursor_pos[0] = client_data[2]
        self.cursor_pos[1] = client_data[3]
        # calculates dx and dy of player bomb
        self.bomb_dx = self.cursor_pos[0] -self.x-2
        self.bomb_dy = self.cursor_pos[1] -self.y-2

        if client_data[4] == 1:
            self.bombs.append(Bomb(self.x + 2, self.y + 2, 3, 3, (255, 255, 0), self.bomb_dx, self.bomb_dy))

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



#all other objects are manipulated through the game object
class Game:

    def __init__(self, player, other_player, map):
        
        #player objects
        self.player = player
        self.other_player = other_player

        #map objects
        self.map = map

        self.pause = 3
        self.text = ""

        self.screen_width = self.map.screen_width


    # gets the player inputs
    def getsInputs(self): 
        self.player.inputs()


    def update(self):
    # updates clients player ------------------------------------------------------------------------------------------------------->
        #checks if there are obstructions to player movement
        if (self.player.y > self.map.map_pieces[self.player.x -3].y +2) or self.player.x <= 10:
            self.player.move_left = False 
            
        if (self.player.y > self.map.map_pieces[self.player.x +3].y +2) or self.player.x >= DISPLAYSURF.get_width() -10:
            self.player.move_right = False

        #jump command for player 
        self.player.jump()
        #moves player left and right
        if self.player.move_right:
            self.player.x += 3
        if self.player.move_left:
            self.player.x -= 3  

        if player1.collision(self.map.map_pieces[player1.x]) or player1.collision(self.map.map_pieces[player1.x + player1.width]):
            player1.y = self.map.map_pieces[player1.x].y - 5
            player1.jumping = False
            player1.jump_vel = player1.jump_height


    # sends a receives player coords and player cursor coords
        self.other_player.set_pos(
            read_data( n.send( make_data( 
                        (round(player1.x),               
                         round(player1.y),               
                         round(player1.cursor_pos[0]),   
                         round(player1.cursor_pos[1]),
                         player1.bomb_init)))
                         )
        ) 
        player1.bomb_init = 0
    # updates bomb ----------------------------------------------------------------------------------------------------------------->
        #gets the pos of player cursor to aim bombs
        self.player.get_cursor(pygame.mouse.get_pos())

        for player in [self.player, self.other_player]:
            for bomb in player.bombs:
                bomb.move()

                # collision for bombs and end of screen
                if bomb.x >= DISPLAYSURF.get_width() or bomb.x <= 0 or bomb.y >= DISPLAYSURF.get_height():
                    bomb.explode()
                    player.bombs.pop()

                elif bomb.collision(self.map.map_pieces[round(bomb.x)]):
                    if bomb.bounces > 0:
                        bomb.bounce()
                    else:
                        bomb.explode()
                        player.bombs.pop()
    
                if bomb.exp_collision(self.player):
                    self.player.lives -= 1


    def draw(self):
        #draws player objects and map
        self.map.draw()
        self.player.draw()
        self.other_player.draw()
       
        #draws bomb objects
        for player in [self.player, self.other_player]:
            for bomb in player.bombs:
                bomb.draw()


    def start_round(self):
        self.map.create_map_obj()


    def end_round(self):
        self.pause = 3
        self.text = self.winner + " has won the round. Restarting in "
        #timer()

    def end_game(self):
        self.pause = 5
        self.text = self.winner + " has won the game. Returning to Title Screen in "
        #timer()
    

    def pause(self):
        if self.pause:
            pass




# colours, represented by RGB colour codes stored as tuples
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
green = (0, 100, 10)

# pygame initialisation
pygame.init()


DISPLAYSURF = pygame.display.set_mode((600, 800)) 
#DISPLAYSURF = pygame.display.set_mode((1200, 800))
# fullscreen off above for testing the multiplayer  
DISPLAYSURF.fill(black)



# initialises the font to be used
pygame.font.init ()
the_font = pygame.font.SysFont("Arial", 10)


# ----------------------------------------------------------------------- Networking --------------------------------------------------------
# helper functions for getting data from the server
def read_data(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])


def make_data(client_data):
    return str(client_data[0]) + "," + str(client_data[1]) + "," + str(client_data[2]) + "," + str(client_data[3]) + "," + str(client_data[4])

def read_map(decoded_string):
    y_variables = []
    decoded_string = decoded_string.split(",")
    for i in decoded_string:
        y_variables.append(int(i))
    return y_variables



# creates object of the network class to join to main server    
n = Network()
startpos = read_data(n.getPos() +",0") # player position will come as a tuple
y_list = read_map(n.getMap()) # map will come as large list

# chooses the player colour based on if the player connected first
if n.id == "0":
    player_colour = red
    other_player_colour = blue

else:
    player_colour = blue
    other_player_colour = red

#---------------------------------------------------------------------------------------------------------------------------------------------------------->



# player objects
player1 = Player(startpos[0], startpos[1], 5, 5, player_colour)
player2 = Player(0, 0, 5, 5, other_player_colour)


# terr is the map object
terr = Map(green)
terr.y_vars = y_list

# stops player from seeing mouse cursor
pygame.mouse.set_visible(False)

game = Game(player1, player2, terr)

game.start_round()

Clock = pygame.time.Clock()



# update loop --------------------------------------------------------------------------------------------------------------------------------------------->
while True:
    # fills the screen black again so sprties actually move
    DISPLAYSURF.fill(black)

    # gets key preses and button presses
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        game.getsInputs()

    game.update()
    game.draw()


    pygame.display.flip()
    Clock.tick(60)
