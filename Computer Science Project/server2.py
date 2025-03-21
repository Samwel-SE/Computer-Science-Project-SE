import socket
from _thread import *
import perlinnoise
import sys
from helperfunctions import convert_round_start_data_to_string, convert_client_position_data_to_string, convert_recv_client_data_to_int


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

print("Server Started")



# player data begins with starting positions of the players and their cursors Ie player.x, player.y, cursor.x, cursor.y
# starting_player_data remains constant so players spawn in the same place at the start of each round with same conditions 
starting_player_data = [(100, 100, 100, 100, 0), (1000, 100, 1000, 100, 0)]


# player data is updated as the round plays out which is why it is initially equal to start_pos as it changes
player_data = [(100, 100, 100, 100, 0),(1000, 100, 1000, 100, 0)]


# -------------------------------------------------------------------- used for sending map data to clients -----------------------------------------------------

# generates list of y variables for pieces of map
def generate_maps():
    # pregame map isnt randomised 
    pre_game_map = [500] * 1300
    
    map_1 = perlinnoise.generate(1300, 25)
    map_2 = perlinnoise.generate(1300, 25)
    map_3 = perlinnoise.generate(1300, 25)
    map_4 = perlinnoise.generate(1300, 25)
    map_5 = perlinnoise.generate(1300, 25)

    # returns map in large list
    return [pre_game_map, map_1, map_2, map_3, map_4, map_5]


# is called when we want to start sending and recieving player data with the client 

def threaded_client(conn, client_num, maps):


    # the map counter variable controls which map is sent to the client from the maps list
    map_counter = 0
    global current_connections
    
    # sends player data to the player client and sends the map data to the player aswell
    try: 
        conn.send(str.encode(convert_round_start_data_to_string(client_num, starting_player_data[client_num], maps[map_counter])))
        reply = ""

    except:
        conn.send(str.encode("server_full"))
        current_connections -= 1
        return "Lost connection, thread closed"
    
    while True:
        try:
            
            # recieves data from client 
            data = conn.recv(4096).decode()

            # checks if there is data or if client wants to disconnect
            if not(data) or data == "DISCONNECT":
                
                # disconnects client by breaking the while loop 
                print("Disconnected")
                break
            

            # data is converted into integer form and stored inside a list
            # [0] and [1] are the clients x and y coords
            # [2] and [3] are the clients cursors x and y coords
            # [4] is the players state_checker variable: used to check if the player has shot a bomb 
            data = convert_recv_client_data_to_int(data)
            
            
            player_data[client_num] = data
            
            if client_num == 1:
                reply = player_data[0]
            else: 
                reply = player_data[1]
                
                #print("recieved: ", data)  for testing server receiving
                #print("Sending: ", reply) for testing server sending
            
            
            
            # if a player hasnt died that state doesn't change and so player just recieves data as normal
            if data[-1] != 2:
                conn.sendall(str.encode(convert_client_position_data_to_string(reply)))


            if current_connections == 2:
            # checks using the state checker variable recieved from client is in state 2 IE a player has been killed
                if data[-1] == 2:
                    map_counter += 1  
                    # turns the data to be sent into string so it can be encoded
                    data_to_be_sent = convert_round_start_data_to_string(client_num, starting_player_data[client_num], maps[map_counter])

                    # chunks the map data into two parts so it doesnt go over the huffer limit
                    data_to_be_sent_prt_1 = data_to_be_sent[0:4096]
                    data_to_be_sent_prt_2 = data_to_be_sent[4096:-1]

                    #print("sending new map")

                    # sends the new map in two parts as stated above
                    conn.sendall(str.encode(data_to_be_sent_prt_1))
                    conn.sendall(str.encode(data_to_be_sent_prt_2))

        except:
            break
    
    current_connections = 0
    return "Lost connection thread closed"
    


def clients_join_server():
    global current_connections
    maps = generate_maps()

    s.listen(2)
    # waits for two connections
    for i in range(2):
        print("waiting for connection")
        conn, addr = s.accept()
        
        print("Connected to: ", addr)

        start_new_thread(threaded_client, (conn, current_connections, maps))
        current_connections += 1



current_connections = 0


while True:
    print("waiting for clients to join server")
    clients_join_server()


