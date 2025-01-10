import socket 

#----------------------------------- THIS IS A SCRIPT I HAVE MODIFIED THE ORIGINGAL VERSION IS WRITTEN BY TECH WITH TIM -----------------------------------


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_ip = "0.0.0.0"
        self.server_port = 4444
        self.addr = (self.server_ip, self.server_port)

        # these variables all start off not being used, but are utilised later

        self.data = "" # sends the player data upon connection to server


        self.id = "" # gets whether player is player 1 or player 2

        self.pos = "" # gets the players position

        self.cursor_pos = "" # gets the players cursor position

        self.state_checker = "" # 3 states; state 0: normal game state / state 1: bomb object is created / state 3: player has been hit

        self.map = "" # gets the map y variables for map pieces
        


    # used for assigning the network obhect to the address of a specific server
    def assign_network_address(self, ip, port):
            self.server_ip = ip
            self.server_port = port
            self.addr = (self.server_ip, self.server_port)

    # get functions -------------------------------------------------
    def getPos(self):
        return self.pos + "," + self.cursor_pos

    def getCursor(self):
        return self.cursor_pos

    def getMap(self):
        return self.map
    # --------------------------------------------------------------


    # client connecting to server
    def connect(self):
        try:
            self.client.connect(self.addr)
            # decodes the data sent from the server
            self.data = self.client.recv(8192).decode()
        except:
            print("failed to connect to that address")
    
            
    # client sending and recieving data from server 
    def send(self, data):
        try:
            # uses data[-1] ie state checker to see if new map data needs to be sent
            if data[-1] != "2":
                self.client.send(str.encode(data))      
                recv_data = self.client.recv(4096).decode()
                self.data = recv_data

            
            #if state checker is on "2" then the new map data is sent
            elif data[-1] == "2":

                self.client.send(str.encode(data))
                
                # chunks the map data into 2 parts as to not go over the buffer limit

                recv_data_1 = self.client.recv(8192).decode()
                recv_data_2 = self.client.recv(8192).decode()
            
                self.data = recv_data_1 + recv_data_2

            self.update_data()

            return self.data
        except socket.error as e:
            print(e)

    def update_data(self):

        self.id = self.data[0] # gets whether player is player 1 or player 2

        self.pos = self.data[2:10] # gets the players position

        self.cursor_pos = self.data[11:19] # gets the players cursor position

        self.state_checker = [20] # 3 states; state 0: normal game state / state 1: bomb object is created / state 3: player has been hit

        self.map = self.data[22:-1] # gets the map y variables for map pieces