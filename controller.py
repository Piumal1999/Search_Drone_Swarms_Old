from network import Network

class Controller:
    def __init__(self):
        self.n = Network()

    def play_step(self, action):
        reply = self.n.send(action)
        return reply

    def connect(self):
        reply = self.n.connect()
        return reply

if __name__ == '__main__':
    c = Controller()
    reply = c.connect()
    print(reply)

    while True:
        action = input("Enter a command: ")
        reply = c.play_step(action)
        print(reply)
