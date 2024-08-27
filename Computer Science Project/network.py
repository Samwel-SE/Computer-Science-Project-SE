import socket 

class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.172"
        self.port = 5555
        self.addr = (self.server, self.port)
        data = self.connect() #connect can only be called once
        self.pos = data[:-1] # gets the players x and y coords
        self.id = data[-1] # gets whether player is player 1 or player 2
        print(self.id)

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            # decodes the data sent from the server
            return self.client.recv(2048).decode() 
        except:
            pass
        
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

