from network import Network

class Controller:
    def __init__(self):
        self.n = Network()

    def play_step(self, action):
        if action == [1, 0, 0, 0, 0]:
            action = "W"
        elif action == [0, 1, 0, 0, 0]:
            action = "S"
        elif action == [0, 0, 1, 0, 0]:
            action = "A"
        elif action == [0, 0, 0, 1, 0]:
            action = "D"
        elif action == [0, 0, 0, 0, 1]:
            action = "0"
        reply = self.n.send(action)
        return reply
    
    def get_state(self):
        reply = self.n.send("state")
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
