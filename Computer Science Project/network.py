import socket 

#----------------------------------- THIS IS A SCRIPT I HAVE MODIFIED THE ORIGINGAL VERSION IS WRITTEN BY TECH WITH TIM -----------------------------------


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #self.server = "192.168.1.173"
        # school wifi IP below
        self.server = "172.17.126.26"
        
        # hotspot IP
        #self.server = "172.20.10.3"

        self.port = 5555
        
        self.addr = (self.server, self.port)
        data = self.connect() #connect can only be called once

        self.id = data[0] # gets whether player is player 1 or player 2

        self.pos = data[1:8] # gets the players position
        self.cursor_pos = data[9:16] # gets the players cursor position

        self.bomb_init = [18]
        
        self.game_mode = [19]

        self.map = data[18:-1] # gets the map y variables for map pieces



    # get functions -------------------------------------------------
    def getPos(self):
        #print(self.pos + "," + self.cursor_pos)
        return self.pos + "," + self.cursor_pos

    def getCursor(self):
        return self.cursor_pos

    def getMap(self):
        #print(self.map)
        return self.map
    # --------------------------------------------------------------


    # client connecting to server ----------------------------------
    def connect(self):
        try:
            self.client.connect(self.addr)
            # decodes the data sent from the server
            return self.client.recv(8192).decode() 
        except:
            pass

    # client sending and recieving data from server -----------------------------------------------------------  
    def send(self, data):
        try:
            self.client.send(str.encode(data))      # sending data
            return self.client.recv(4096).decode()  # receiving data
        except socket.error as e:
            print(e)
    #-----------------------------------------------------------------------------------------------------------