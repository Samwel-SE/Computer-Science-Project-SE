import socket 

#----------------------------------- THIS IS A SCRIPT I HAVE MODIFIED THE ORIGINGAL VERSION IS WRITTEN BY TECH WITH TIM -----------------------------------


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

        # home wifi
        self.server = "192.168.1.174"
        
        
        # school wifi IP below
        # self.server = "172.17.126.26"
        
        # hotspot IP
        #self.server = "172.20.10.3"

        self.port = 5555
        
        self.addr = (self.server, self.port)

        # begin game is set to true as when the client first connects the game has just began
        self.begin_game = True 

        self.data = self.connect() # sends the player data upon connection to server


        self.id = self.data[0] # gets whether player is player 1 or player 2

        self.pos = self.data[2:8] # gets the players position

        self.cursor_pos = self.data[10:16] # gets the players cursor position

        self.state_checker = [18] # 3 states; state 0: normal game state / state 1: bomb object is created / state 3: player has been hit

        self.map = self.data[20:-1] # gets the map y variables for map pieces
        


    # get functions -------------------------------------------------
    def getPos(self):
        #print(self.pos + "," + self.cursor_pos)
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
            return self.client.recv(8192).decode() 
        except:
            pass
    
            
    # client sending and recieving data from server 
    def send(self, data):
        try:
            if data[-1] != 2:
                self.client.send(str.encode(data))      
                recv_data = self.client.recv(4096).decode()
            
            else:
                self.client.send(str.encode(data))
                recv_data = self.client.recv(16384).decode()
            
            self.data = recv_data
            self.update_data()

            return self.data
        except socket.error as e:
            print(e)
    

    # client just recieving data from the server 
    # def recieve_data(self):
    #     try:
    #         print("recieve data being called")
    #         data_part_1 = self.client.recv(8196).decode()
    #         # data_part_2 = self.client.recv(8196).decode() 
    #         # data_part_3 = self.client.recv(8196).decode()
            
    #         self.data = data_part_1
    #         print(self.data)
    #         return self.data


    #     except socket.error as e:
    #         print(e)

    # this updates the data of the player so it isnt just using the same data as before the start of the new round 
    def update_data(self):

        self.id = self.data[0] # gets whether player is player 1 or player 2

        self.pos = self.data[2:8] # gets the players position

        self.cursor_pos = self.data[10:16] # gets the players cursor position

        self.state_checker = [18] # 3 states; state 0: normal game state / state 1: bomb object is created / state 3: player has been hit

        self.map = self.data[20:-1] # gets the map y variables for map pieces