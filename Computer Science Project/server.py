import socket
from _thread import *
import perlinnoise
import random
import sys



# ---------------------------- THIS IS A SCRIPT I HAVE MODIFIED, THE ORIGINAL SCRIPT IS WRITTEN BY TECH WITH TIM ---------------------------#


#server = "192.168.1.173" 
# only use below if on school wifi
server = "172.17.126.26"  

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)


s.listen(2)
print("Waiting for connection, Server Started")

# starting positions of the players and their cursors Ie player.x, player.y, cursor.x, cursor.y
player_data = [(100, 100, 0, 0), (400, 100, 0, 0)] 



# -------------------------------------------------------------------- used for sending map data to clients -----------------------------------------------------

# generates list of y variables for pieces of map
def generate_list():
        y_list = perlinnoise.generate(1600, 40)
        return y_list


# puts map data into string form
def make_map(y_list):
    encoded_string = ""
    for i in y_list: encoded_string = encoded_string + str(i) + ","
    encoded_string = encoded_string[:-1]
    return encoded_string


# function for sending map data as a string to clients to be decoded
def round_start_data(tup, id, map):
    return str(id) + str(tup[0]) + "," + str(tup[1]) + str(tup[2]) + "," + str(tup[3]) + "," + make_map(map)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------- helper functions for sending and decoding data -----------------------#
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])
# ------------------------------------------------------------------------------------------#


#pre game lobby map
pre_game_map = [500] * 1600

#maps for the rounds of the game.
map_1 = generate_list()
map_2 = generate_list()
map_3 = generate_list()


def threaded_client(conn, client_num):
    conn.send(str.encode(round_start_data(player_data[client_num], client_num, pre_game_map)))
    reply = ""
    
    while True:
        try:
            data = read_pos(conn.recv(4096).decode())
            player_data[client_num] = data

            if not(data):
                print("Disconnected")
                break
            else:
                if client_num == 1:
                    reply = player_data[0]
                else: 
                    reply = player_data[1]
                #print("recieved: ", data)  for testing server receiving
                #print("Sending: ", reply) for testing server sending

            conn.sendall(str.encode(make_pos(reply)))

        except:
            break
        
    print("Lost Connection")
    conn.close()

currentClient = 0
# while loop will continuously listen for connections
while True:
    # accepts any incoming connections and stores the conn and IP addr in the two variables
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentClient))
    currentClient += 1 




