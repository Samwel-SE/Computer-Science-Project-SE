import socket
from _thread import *
import perlinnoise
import sys



# ---------------------------- THIS IS A SCRIPT I HAVE MODIFIED, THE ORIGINAL SCRIPT IS WRITTEN BY TECH WITH TIM ---------------------------#


#server = "192.168.1.173" 

# only use below if on school wifi
server = "172.17.126.26"  

# hotspot IP
#server = "172.20.10.3"

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)


s.listen(2)
print("Waiting for connection, Server Started")

# starting positions of the players and their cursors Ie player.x, player.y, cursor.x, cursor.y
#player_data = [(100, 100, 100, 100), (400, 100, 400, 100)] 
player_data = [(100,100,100,100,0), (400,100,400,100,0)]


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
def round_start_data(client_data, id, map):
    return str(id) + make_data(client_data) + make_map(map)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------- helper functions for encoding and decoding data -----------------------#
# decodes the data from string form
def read_data(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])

# encodes the data into string form to send to the clients
def make_data(client_data):
    return str(client_data[0]) + "," + str(client_data[1]) + "," + str(client_data[2]) + "," + str(client_data[3]) + "," + str(client_data[4])
# ------------------------------------------------------------------------------------------#


# pre game lobby map
pre_game_map = [500] * 1600

# maps for the rounds of the game
map_1 = generate_list()
map_2 = generate_list()
map_3 = generate_list()


def threaded_client(conn, client_num):
    # sends player data to the player client and sends the map data to the player aswell
    conn.send(str.encode(round_start_data(player_data[client_num], client_num, map_1)))
    reply = ""
    
    while True:
        try:
            data = read_data(conn.recv(4096).decode())
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

            conn.sendall(str.encode(make_data(reply)))

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




