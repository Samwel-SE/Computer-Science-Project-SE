import sys

import pygame
from pygame.locals import QUIT

from network import Network


from helperfunctions import convert_recv_client_data_to_int, convert_client_data_to_string, convert_recv_map_data_to_int
import time

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
        self.pieces = []

        # stores y variables of all the objects making up the map
        self.y_vars = 0
        self.piece_length = 700

    # creates map obj
    def create_map_obj(self):
        self.pieces.clear()
        for i in range(len(self.y_vars)):
            self.pieces.append(GameObject(i, self.y_vars[i], 1, self.piece_length, self.colour))

    # iterates through and draws all the gameobjects making up the map
    def draw(self):
        for i in range(len(self.y_vars)):
            self.pieces[i].draw()




# Title screen object
class Title_Screen:

    def __init__(self):
        
        # x coord of text so its alligned with center of screen
        self.x_pos = DISPLAYSURF.get_width()//2 - 100

        self.join_server_1_button = Button(self.x_pos, 300, 220, 30, white)

        self.join_server_2_button = Button(self.x_pos, 400, 220, 30, white)

        self.quit_game_button = Button(self.x_pos, 500, 220, 30, white)

        self.open = True


    # to be called in the input function of game object
    def handle_button_presses(self):

        if self.join_server_1_button.on_click():
            
            # you join the server 
            if join_server(5555):
                self.open = False

            # you dont join the server
            else:
                self.join_server_1_button.error_text_on = True    

        if self.join_server_2_button.on_click(): 
            
            # you join the server
            if join_server(6666):
                self.open = False
            
            # you dont join the server
            else:
                self.join_server_2_button.error_text_on = True

        if self.quit_game_button.on_click():
            quit()



    # draws the title screen
    def draw(self):
        # draws game title 
        DISPLAYSURF.blit(text.render("SQUARE OFF", False, white), (self.x_pos, 100))
        
        # draws join_server 1 button
        DISPLAYSURF.blit(text.render("Join Server 1", False, white), (self.x_pos, 300))
        self.join_server_1_button.draw()

        # draws join_server 2 button
        DISPLAYSURF.blit(text.render("Join Server 2", False, white), (self.x_pos, 400))
        self.join_server_2_button.draw()


        # draws quit game button
        DISPLAYSURF.blit(text.render("Quit Game", False, white), (self.x_pos, 500))
        self.quit_game_button.draw()


# button class is used in the title screen
class Button(GameObject):

    def __init__(self, x, y, width, height, colour):
        super().__init__(x, y, width, height, colour)

        self.error_text_on = False

    # draws the border rectangle of the button, with 1 pixel border width
    # this is why it cannot inherit draw method from parent as it doesn't fill rectangle
    def draw(self):
        pygame.draw.rect(DISPLAYSURF, self.colour, pygame.Rect(self.x, self.y, self.width, self.height), 1)

        if self.error_text_on:
            DISPLAYSURF.blit(text.render("Server Full. Try Join another server", False, red), (self.x, self.y + 50))


    # runs certain code once the button has been pressed
    def on_click(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(3) and (mouse_x > self.x and mouse_x < self.x +self.width) and (mouse_y > self.y and mouse_y < self.y + self.height):
                return True


#### PLAYER OBJECT #############################################################################################################
# player class inherits gameobject class
class Player(GameObject):
    
    def __init__(self, x, y, width, height, colour, ui_x_coord):
        super().__init__(x, y, width, height, colour)

        # user interface x coordinate
        self.ui_x_coord = ui_x_coord

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
        self.state_checker = 0

        # bullet direction x and y
        self.bomb_dx = 0
        self.bomb_dy = 0
        
        # Number of lives player has
        self.lives = 3
        

    # adds drawing player cursor, life count and currently equipped weapon
    def draw(self):
        super().draw()

        # draws players cursor
        pygame.draw.line(DISPLAYSURF, self.colour, (self.x + 2, self.y + 2), self.cursor_pos,1)

        #draws player live count
        for i in range(self.lives):
            pygame.draw.rect(DISPLAYSURF, self.colour, pygame.Rect(self.lives + i*10 + self.ui_x_coord, 0, 5, 10))


    # upates the position of the player
    def update(self, pieces):
        
        # collision between parts of terrain that are too high for the player to climb or the edge of the screen
        if (self.y > pieces[self.x -3].y +2) or self.x <= 10:
            self.move_left = False 
                    
        elif (self.y > pieces[self.x +3].y +2) or self.x >= DISPLAYSURF.get_width() -10:
            self.move_right = False

        # jump command for player 
        self.jump()
        
        # moves player left and right
        if self.move_right:
            self.x += 3
        if self.move_left:
            self.x -= 3

        # collision so that player does not fall through the map
        if self.collision(pieces[self.x]) or self.collision(pieces[self.x + self.width]):
                self.y = pieces[self.x].y - 5
                self.jumping = False
                self.jump_vel = self.jump_height


    # gets keys currently pressed so player character can move
    def inputs(self):

        # movement inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.move_right = True
            if event.key == pygame.K_a:
                self.move_left = True
            if event.key == pygame.K_w and self.jumping == False:
                self.jumping = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                self.move_right = False
            if event.key == pygame.K_a:
                self.move_left = False

        # Once the left mouse button is pressed and there are no other bombs on screen will create a bomb object,
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if other_player_joined():
                if pygame.mouse.get_pressed(3) and len(self.bombs) == 0 and (self.state_checker != 9):
                    self.state_checker = 1


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
    def get_cursor(self, mouse_tuple):

        # diff dict stores the difference in x & y between cursor pos and mouse pos
        diff = {"x": abs(mouse_tuple[0] -self.x) *0.04, "y": abs(mouse_tuple[1] -self.y) *0.04}
        
        if mouse_tuple[0] >= (self.x + 2): 
           self.bomb_dx = diff["x"]
        else: 
            self.bomb_dx = -diff["x"]

        if mouse_tuple[1] <= (self.y + 2): 
            self.bomb_dy = -diff["y"]
        else: 
            self.bomb_dy = diff["y"]
        
        # rounds the bomb dx and dy to the nearest integer
        self.bomb_dx = round(self.bomb_dx) 
        self.bomb_dy = round(self.bomb_dy)
        
        # then sets the coordinates of the cursor
        self.cursor_pos = [self.bomb_dx +self.x+2 , self.bomb_dy +self.y+2]

        # and returns it
        return self.cursor_pos


    # function is used to control the client player in host players game
    def set_player_variables(self, client_data):
        
        # coords 
        self.x = client_data[0]
        self.y = client_data[1]

        # cursor coords
        self.cursor_pos = [client_data[2], client_data[3]]
        
        # state checker
        self.state_checker = client_data[4]


    # checks whether bomb needs to be created
    def check_bomb_creation(self, bomb_creation_on_1):
        
        # if clients bomb_init equals 1 it will append a bomb object to other_players bomb list so it is drawn on the screen
        if bomb_creation_on_1 == 1:
            
            # calculates dx and dy of player bomb from cursor_position
            self.bomb_dx = self.cursor_pos[0] -self.x-2
            self.bomb_dy = self.cursor_pos[1] -self.y-2
            
            self.bombs.append(Bomb(self.x + 2, self.y + 2, 3, 3, (255, 255, 0), self.bomb_dx, self.bomb_dy))

########################################################################################################################################


###### BOMB OBJECT ###########################################################################################################################

# Bomb class, inherits Game Object Class
class Bomb(GameObject):

    def __init__(self, x, y, width, height, colour, dx, dy):
        super().__init__(x, y, width, height, colour)
        
        # change in x and y Ie movement speed of bomb
        self.dx = dx
        self.dy = dy
        
        # radius of bomb explosion
        self.exp_rad = 50
        
        # state of bomb: moving or exploded
        self.state = "moving"


    # movement of the bomb
    def update(self, pieces):

        # increments the bombs x coordinate
        self.x += self.dx

        # increments the bombs y coordinate
        self.y += self.dy
        self.dy += 1

        # collision for bombs and end of screen
        if self.x >= DISPLAYSURF.get_width() or self.x <= 0:
            self.explode()
        

        # code below means bomb will bounce after colliding with the map
        elif self.collision(pieces[self.x]):
            self.explode()



    def draw(self):
        if self.state == "exploded":
            # rgb code used below is colour orange
            pygame.draw.circle(DISPLAYSURF, (255, 165, 0), (self.x+1, self.y+1), self.exp_rad)
        else:

            # if the state isn't exploded it will just draw the bomb obj as a yellow square
            super().draw()


    # draws the expxlosion of the bomb
    def explode(self):
        self.state = "exploded"

    # checks whether points of other objects overlap with explosion, returning True or False
    def exp_collision(self, obj2):
        if ((self.x -1)- obj2.x) ** 2 + ((self.y +1) - obj2.y) ** 2 <= self.exp_rad**2:
            return True

##############################################################################################################################################




#all other objects are manipulated through the game object
class Game:

    def __init__(self, player, other_player, map):
        
        #player objects
        self.player = player
        self.other_player = other_player

        #map object
        self.map = map

        # life of the interim round
        self.interim_round_life = 1

        self.screen_width = self.map.screen_width

        self.text = "INTERIM ROUND ... WEAPONS DISABLED TILL OTHER PLAYER JOINS"

        
        

    # gets the player inputs
    def getsInputs(self): 
        # only checks for player inputs when the game isn't paused
        self.player.inputs()


    # transfers clients data and map data
    def transfer_data(self):
    
        return n.transfer( 
                    convert_client_data_to_string(
                        (
                        self.player.x,               
                        self.player.y,               
                        self.player.cursor_pos[0],   
                        self.player.cursor_pos[1],
                        self.player.state_checker
                        )                        
                    )
                )
    
    # updates the objects in the game
    def update(self):
        

        # updates player position
        self.player.update(self.map.pieces)


        # gets player cursor so bomb can be updated correctly
        self.player.get_cursor(pygame.mouse.get_pos())


        # checks whether bombs are created for the players
        self.player.check_bomb_creation(self.player.state_checker)
        self.other_player.check_bomb_creation(self.other_player.state_checker)


        # updates bomb ----------------------------------------------------------------------------------------------------------------->
        for p in [self.player, self.other_player]:
            
            for bomb in p.bombs:
                
                bomb.update(self.map.pieces)
                
                for player in [self.player, self.other_player]:
                    # for when a player is within explosion radius
                    if bomb.exp_collision(player) and bomb.state == "exploded":
                        
                        # so a player doesnt lose a life in the interim round
                        if self.interim_round_life > 0:
                            self.interim_round_life -= 1

                        else:    
                            # player loses life if it has been hit
                            player.lives -= 1
                        

                        # when player has 0 lives the end_game is called
                        if player.lives == 0:
                            self.end_game()

                        # if the player has more than 0 lives game continues, end round called instead
                        else:
                            self.end_round()

        # transfers player data and updates the enemy clients player on your screen

        self.other_player.set_player_variables(
            convert_recv_client_data_to_int(self.transfer_data())
        ) 

        # resets state checker back to 0 at the end of every update loop so that only bomb object is created
        self.player.state_checker = 0


    def draw(self):
        
        #draws player objects and map
        self.map.draw()
        self.player.draw()
        self.other_player.draw()
    
        #draws bomb objects
        for player in [self.player, self.other_player]:
            for bomb in player.bombs:
                bomb.draw()
                
                # deletes the bomb obj once it has exploded
                if bomb.state == "exploded":
                    player.bombs.pop()


        
            # draws text for the begining of game, ends of rounds and the end of the game
            DISPLAYSURF.blit(text.render(self.text, False, white), (200, 200))

    
    def start_round(self):
        # sets state checker to "2" to tell server to send next map
        self.player.state_checker = 2

        # then sends data to server which sends back new map as game is going into next round
        self.transfer_data()
        
        # gets the map data 
        map_data = n.getMap()

        # sets state checker back to 0 so server doesn't update map again
        self.player.state_checker = 0

        # creates the new map object for the game
        self.map.y_vars = convert_recv_map_data_to_int(map_data)
        self.map.create_map_obj()
        
        # sets the player client back to its starting position and sets the player clients state checker to 0
        player_data = convert_recv_client_data_to_int(n.getPos())
        self.player.set_player_variables(player_data)
        
        # removes all getInputs events from queue so no bomb objects 
        pygame.event.clear()

    
    # pauses the game for 5 seconds and renders end round / game text
    def pause_game(self):
        
        for i in range(5):
            
            # adds the time length left of timer to the end round text
            self.text = self.text + " " + str(5-i)
            DISPLAYSURF.fill(black)

            self.draw()
            pygame.display.flip()
            time.sleep(1)

    def end_round(self):
        
        self.text = f"A player has lost the round. Next Round starting in "
        self.pause_game()
            
        # then sets the text back to nothing so text is not drawn whilst game is running and starts the next round
        self.player.jumping = False
        self.other_player.jumping = False
        self.text = ""
        self.start_round()


    def end_game(self):
        
        self.text = "A player has lost the game. You will be returned to Main Menu in "
        # starts a 5 second count down for end of game 
        self.pause_game()
        
        n.leave_server()

        global main_menu
        main_menu.open = True

        self.text = "INTERIM ROUND ... WEAPONS DISABLED TILL OTHER PLAYER JOINS"
        self.player.lives = self.other_player.lives = 3
        self.interim_round_life = 1
        
        # turns the mouse back on so player can interact with the title screen
        pygame.mouse.set_visible(True)

# ----------------------------------------------------------------------- Networking --------------------------------------------------------


def join_server(server_address):
    
    global n 

    n = Network()
    
    #school ip
    server_ip = "172.17.126.26"
    
    #home ip 
    #server_ip = "192.168.1.174"

    n.assign_network_address(server_ip, server_address)
    if n.connect() == "connection success":
        n.update_client_data_for_network()

        # n.getPos only returns 4 values so we need to prematurely append a 0 to act as the state for the startpos
        startpos = convert_recv_client_data_to_int(n.getPos())

        # chooses the player colour based on if the player connected first

        # if player joins first they are the red player and their UI is in the top left
        if n.id == "0":
            player1.colour = red
            player2.colour = blue
            
            player1.ui_x_coord = 0
            player2.ui_x_coord = DISPLAYSURF.get_width() -50
        
        # if the player joins the game second they are the blue player and their UI is in the top right
        else:
            player1.colour = blue
            player2.colour = red
            
            player1.ui_x_coord = DISPLAYSURF.get_width() -50
            player2.ui_x_coord = 0
        
        # sets the player objects up
        player1.x, player1.y = startpos[0], startpos[1]
        player2.x, player2.y = startpos[0], startpos[1]

        # sets the map object up
        terr.y_vars = convert_recv_map_data_to_int(n.getMap())
        terr.create_map_obj()

        # stops player from seeing mouse cursor so has to use in game cursor to aim
        pygame.mouse.set_visible(False)
        return True
    else:
        return False



# checks whether or not the other player has joined
def other_player_joined():
    if (player2.x -1000 == 0) and (player2.y -100 == 0):
        return False
    return True



#---------------------------------------------------------------------------------------------------------------------------------------------------------->


# colours, represented by RGB colour codes stored as tuples
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
green = (0, 100, 10)


 
# pygame initialisation
pygame.init()

# INITIALISING DISPLAY SURFACE
DISPLAYSURF = pygame.display.set_mode((1200, 800))
DISPLAYSURF.fill(black)

pygame.display.set_caption('SQUARE OFF')


# initialises the font to be used
pygame.font.init()

text = pygame.font.SysFont("Arial", 20)


# player objects
player1 = Player(0, 0, 5, 5, red, 0)
player2 = Player(0, 0, 5, 5, red, 0)


# terr is the map object
terr = Map(green)
terr.y_vars = [0]


# creates the title screen for the game where the user chooses to host, join or quit
main_menu = Title_Screen()


# initialises game object with 
game = Game(player1, player2, terr)


Clock = pygame.time.Clock()


def Quitting_Game(trigger):
    if trigger.type == "QUIT":
        pygame.quit()
        sys.exit()

# MAIN GAME LOOP ################################################################################

while True:
    # fills the screen black again so sprties actually move
    DISPLAYSURF.fill(black)


    # only runs this code if the main menu of the game is open
    if main_menu.open:
        for event in pygame.event.get():
            #quits the game
            Quitting_Game(event)
            main_menu.handle_button_presses()
        
        # draws the title screen
        main_menu.draw()
        pygame.display.flip()

        
        # tick rate is set to 60: screen is updated 60 times a second
        Clock.tick(60)
    

    # runs this code when the main menu is closed Ie playing the game after joining a server
    else:
        # gets key preses and button presses
        for event in pygame.event.get():
            # quits the game
            Quitting_Game(event)

            #gets the inputs from clients machine
            game.getsInputs()

        # updates game
        game.update()

        #draws the game and its agregate objects
        game.draw()
        pygame.display.flip()
      
        # tick rate is set to 60: screen is updated 60 times a second
        Clock.tick(60)
