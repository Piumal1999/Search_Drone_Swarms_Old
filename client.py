import socket
import sys

class Client:
    def __init__(self, port):
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', self.port)

    def send_command(self, command):
        try:
            self.client.sendto(command.encode(), self.server_address)
        except:
            print("Error sending command.")

if __name__ == '__main__':
    port = int(sys.argv[1])
    client = Client(port)

    while True:
        command = input("Enter command (W/A/S/D): ")
        if command in ['W', 'A', 'S', 'D']:
            client.send_command(command)
        else:
            print("Invalid command. Use WASD.")
