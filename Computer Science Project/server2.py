import socket
from _thread import *
import perlinnoise

# ---------------------------- THIS IS A SCRIPT I HAVE MODIFIED, THE ORIGINAL SCRIPT IS WRITTEN BY TECH WITH TIM ---------------------------#


# home wifi
server = "0.0.0.0" 

# server 2 port
port = 6666

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)


# listens for connections
s.listen(2)

print("Server Started, Waiting for connection")


# starting positions of the players and their cursors Ie player.x, player.y, cursor.x, cursor.y
# start_pos remains constant so players spawn in the same place at the start of each round
start_pos = [(100,100,100,100,0), (1000,100,1000,100,0)]

# player data is updated as the round plays out which is why it is initially equal to start_pos as it changes
player_data = start_pos


# -------------------------------------------------------------------- used for sending map data to clients -----------------------------------------------------

# generates list of y variables for pieces of map
def generate_map():
    y_list = perlinnoise.generate(1300, 25)
    return y_list


# puts map data into string form
def stringify_map(y_list):
    encoded_string = ""
    for i in y_list: 
        encoded_string = encoded_string + str(i) + ","
    encoded_string = encoded_string[:-1]
    return encoded_string


# function for sending map data as a string to clients to be decoded
def stringify_round_start_data(client_id, client_data, map_data):
    return str(client_id) + "," + stringify_position_data(client_data) + "," + stringify_map(map_data)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------



# ------------------- helper functions for encoding and decoding data --------------------------------------------------------------------------#
# decodes the data from string form
def read_data(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4])



# encodes the data into string form to send to the clients
def stringify_position_data(client_data):
    stringified_data = []
    for i in [0,2]:
        if len(str(client_data[i])) < 4:
            stringified_data.append("0" + str(client_data[i]))
        else:
            stringified_data.append(str(client_data[i]))
    return stringified_data[0] + "," + str(client_data[1]) + "," + stringified_data[1] + "," + str(client_data[3]) + "," + str(client_data[4])
# -----------------------------------------------------------------------------------------------------------------------------------------------#

# pre game lobby map
pre_game_map = [500] * 1300

# maps for the rounds of the game
map_1 = generate_map()
map_2 = generate_map()
map_3 = generate_map()
map_4 = generate_map()
map_5 = generate_map()



# variables to control which map is displayed
maps = [pre_game_map, map_1, map_2, map_3, map_4, map_5]

def threaded_client(conn, client_num):
    # the map counter variable controls which map is sent to the client from the maps list
    map_counter = 0
    
    # sends player data to the player client and sends the map data to the player aswell
    conn.send(str.encode(stringify_round_start_data(client_num, player_data[client_num],maps[map_counter])))
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
            
            
            # if a player hasnt died that state doesn't change and so player just recieves data as normal
            if data[-1] != 2:
                conn.sendall(str.encode(stringify_position_data(reply)))

            # checks using the state checker variable recieved from client is in state 2 IE a player has been killed
            elif data[-1] == 2:
                map_counter += 1  
                print("starting round pos " + f"{start_pos[client_num]}")
                # turns the data to be sent into string so it can be encoded
                data_to_be_sent = stringify_round_start_data(client_num, [(100, 100, 100, 100, 0),(1000, 100, 1000, 100, 0)][client_num], maps[map_counter])

                # chunks the map data into two parts so it doesnt go over the huffer limit
                data_to_be_sent_prt_1 = data_to_be_sent[0:4096]
                data_to_be_sent_prt_2 = data_to_be_sent[4096:-1]

                print("sending new map")

                # sends the new map in two parts as stated above
                conn.sendall(str.encode(data_to_be_sent_prt_1))
                conn.sendall(str.encode(data_to_be_sent_prt_2))

        except:
            break
    
    print("Lost Connection")
    conn.close()
    quit()

currentClient = 0
# while loop will continuously listen for connections
while True:
    # accepts any incoming connections and stores the conn and IP addr in the two variables
    conn, addr = s.accept()

    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentClient))
    currentClient += 1 

