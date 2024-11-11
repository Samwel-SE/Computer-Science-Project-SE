import socket
from _thread import *
import perlinnoise
import random
import sys

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

# starting positions of the players and their cursors
pos = [(100, 100, 0, 0), (400, 100, 0, 0)] 


# helper functions for getting data from the server
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

def make_data(tup, id, map):
    return str(id) + str(tup[0]) + "," + str(tup[1]) + str(tup[2]) + "," + str(tup[3]) + "," + make_map(map)


# -------------------------------------------------------------------- used for sending map data to clients -----------------------------------------------------
# generates list of y variables for map pieces
def generate_list():
        y_list = perlinnoise.generate(1600, random.randint(50, 60))
        return y_list

def make_map(y_list):
    encoded_string = ""
    for i in y_list: encoded_string = encoded_string + str(i) + ","
    encoded_string = encoded_string[:-1]
    return encoded_string
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------




temp_var = generate_list()

def threaded_client(conn, player):
    conn.send( str.encode(make_data(pos[player], player, temp_var)) )
    reply = ""
    
    while True:
        try:
            data = read_pos(conn.recv(4096).decode())
            pos[player] = data

            if not(data):
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else: 
                    reply = pos[1]
                #print("recieved: ", data)
                #print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))

        except:
            break
        
    print("Lost Connection")
    conn.close()

currentPlayer = 0
# while loop will continuously listen for connections
while True:
    # accepts any incoming connections and stores the conn and IP addr in the two variables
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1 




