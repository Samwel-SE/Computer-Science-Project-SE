import socket 

#----------------------------------- THIS IS A SCRIPT I HAVE MODIFIED THE ORIGINGAL VERSION IS WRITTEN BY TECH WITH TIM -----------------------------------


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.173"
        # school wifi IP below
        # self.server = "172.17.126.26"
        self.port = 5555
        self.addr = (self.server, self.port)
        data = self.connect() #connect can only be called once

        self.id = data[0] # gets whether player is player 1 or player 2

        self.pos = data[1:7] # gets the players position
        self.cursor_pos = data[9:14] # gets the players cursor position

        


        self.map = data[16:-1] # gets the map y variables for map pieces



    # get functions -------------------------------------------------
    def getPos(self):
        return self.pos + "," + self.cursor_pos

    def getCursor(self):
        return self.cursor_pos

    def getMap(self):
        return self.map
    # --------------------------------------------------------------


    # client connecting to server ----------------------------------
    def connect(self):
        try:
            self.client.connect(self.addr)
            # decodes the data sent from the server
            return self.client.recv(4096).decode() 
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