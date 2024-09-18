import socket
from _thread import *
import sys

#server = "192.168.1.174" 
# only use below if hotspotting
server = "172.20.10.3"  

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)

s.listen(2)
print("Waiting for connection, Server Started")

# starting positions of the players
pos = [(100, 100), (400, 100)] 


# helper functions for getting data from the server
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def make_data(tup, id):
    return str(tup[0]) + "," + str(tup[1]) + str(id)


def threaded_client(conn, player):
    conn.send(str.encode(make_data(pos[player], player)))
    reply = ""

    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not(data):
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else: 
                    reply = pos[1]
                print("recieved: ", data)
                print("Sending: ", reply)

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




