import json

from model import Model
import socket
import jpysocket


class Server:
    def __init__(self):
        self.host = socket.gethostbyname_ex(socket.gethostname())[2][1]
        self.port = 8080
        self.maxConnections = 5

        print("Host: " + self.host)

    def start(self):
        self.setup()
        self.mainLoop()

    def setup(self):
        self.server = socket.socket()
        self.server.bind((self.host, self.port))
        self.server.listen(self.maxConnections)
        print("Socket Is Listening....")

    def predict(self, game, index):
        temp = self.model.to_list(self.model.recommend_games(game))[index]
        return temp

    def getInfo(self, game):
        temp = self.model.getInfo(game)
        return temp

    def mainLoop(self):
        while True:
            self.model = Model()
            connection, address = self.server.accept()
            print("Connected To ", address)
            msgrecv = connection.recv(1024)
            msgrecv = jpysocket.jpydecode(msgrecv)
            print("From Client: ", msgrecv)

            if msgrecv[0] == "$":
                try:
                    print(msgrecv.lstrip("$"))
                    msgsend = jpysocket.jpyencode(str(self.getInfo(msgrecv.lstrip("$"))))
                    print(msgsend)
                except:
                    print("Invalid input")
            else:
                try:
                    game = str(msgrecv.split("$")[0])
                    index = int(msgrecv.split("$")[1])
                    msgsend = jpysocket.jpyencode(str(self.predict(game, index)))
                except:
                    print("Invalid input")
            connection.send(msgsend)