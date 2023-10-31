import pygame
from constants import *
from utils import *
from grid import GridField
from vehicle import Vehicle
import csv
import socket
from _thread import *
import json

vec2 = pygame.math.Vector2

pygame.init()

class Simulation(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

        # npc target
        self.npc = Npc_target()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.npc)

        self.reset_simulation()

    def reset_simulation(self):
        try:
            for _ in self.swarm:
                del _
        except:
            pass

        self.score = 0
        self.target_simulation = None

        # reset grid
        self.grid_field = GridField(RESOLUTION)

        # variables for swarm
        self.swarm = []
        self.create_swarm_uav()

        # get target from obs.csv
        with open('obs.csv', 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, val in enumerate(row):
                    if val == 'X':
                        self.target_simulation = self.grid_field.get_cell_center([j, i])

    def create_swarm_uav(self):
        # get spawn locations from obs.csv
        spawn_locations = []
        with open('obs.csv', 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, val in enumerate(row):
                    if val == '+':
                        spawn_locations.append(self.grid_field.get_cell_center([j, i]))

        # create 1 drone each in every location
        for location in spawn_locations:
            drone = Vehicle(location.x, location.y, self.screen)
            self.swarm.append(drone)

    def update_ui(self):

        background_image = pygame.image.load("models/texture/camouflage.png").convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Background
        self.screen.fill(LIGHT_BLUE)
        self.screen.blit(background_image, [0, 0])

        # draw grid of visited celss
        self.grid_field.draw(self.screen)

        # draw target - npc
        if self.target_simulation:
            self.all_sprites.draw(self.screen)
            self.all_sprites.update(self.target_simulation, 0)
            pygame.draw.circle(self.screen, LIGHT_BLUE, self.target_simulation, RADIUS_TARGET, 2)

        for drone in self.swarm:
            drone.draw(self.screen)

        pygame.display.flip()

    def is_collision(self):
        """
            Checks if drone is colliding with another drone or with the limits of the screen or with an obstacle cell
            do not use functions from vehicle.py
        """
        for _ in self.swarm:
            for __ in self.swarm:
                if _ != __:
                    if _.location == __.location:
                        return True

            if _.location.x < 0 or _.location.x > SCREEN_WIDTH or _.location.y < 0 or _.location.y > SCREEN_HEIGHT:
                return True

            # check if cell is obstacle
            cell = self.grid_field.get_cell_when_xy_is_given(_.location.x, _.location.y)
            if cell.state == 1:
                return True

        return False
    
    def is_target_found(self):
        """
            Checks if the drones found the target
        """
        for _ in self.swarm:
            if not _.reached_goal(self.target_simulation):
                return False

        return True
    
    def is_blocked_cell(self, col, row):
        """
            Checks if the cell is blocked
        """
        if self.grid_field.get_state_cell([col, row]) == 1:
            return True
        else:
            # blocked by a drone
            for _ in self.swarm:
                if int(_.location.x / RESOLUTION) == col and int(_.location.y / RESOLUTION) == row:
                    return True
        
        return False
    
    def get_state(self, player):
        col = int(self.swarm[player].location.x / RESOLUTION)
        row = int(self.swarm[player].location.y / RESOLUTION)

        state = [
            self.is_blocked_cell(col-1, row-1),
            self.is_blocked_cell(col, row-1),
            self.is_blocked_cell(col+1, row-1),
            self.is_blocked_cell(col-1, row),
            self.is_blocked_cell(col+1, row),
            self.is_blocked_cell(col-1, row+1),
            self.is_blocked_cell(col, row+1),
            self.is_blocked_cell(col+1, row+1),

            # is target left, right, top, bottom
            self.swarm[player].location.x < self.target_simulation.x,
            self.swarm[player].location.y < self.target_simulation.y
        ]

        return state
    
    def get_score(self, player):
        # if self.swarm[player].location.distance_to(self.target_simulation) < RADIUS_TARGET:
        #     score = RADIUS_TARGET - (self.target_simulation - self.swarm[player].location).length()
        # else:
        #     score = 0

        score = 0
        for _ in self.swarm:
            if _.location.distance_to(self.target_simulation) < RADIUS_TARGET:
                score += RADIUS_TARGET - (self.target_simulation - _.location).length()
            else:
                score += 0

        return score

    def connect_controller(self, conn, player):
        conn.send(str.encode("Connected"))
        reply = ""
        while True:
            try:
                action = conn.recv(2048).decode()

                if not action:
                    print("Disconnected")
                    break
                elif action == "state":
                    reply = self.get_state(player)
                    print("Sending state: ", reply, "to player", player)
                else:
                    reply = {
                        "game_over": False,
                        "score": self.get_score(player),
                        "reward": 5
                        }
                    print("Received: ", action)
                    self.swarm[player].move(action)
                    self.swarm[player].moves += 1

                    if self.is_collision() or self.swarm[player].moves > 100:
                        reply["game_over"] = True
                        reply["reward"] = -100
                        print("Game over due to collision or moves > 100")
                        self.reset_simulation()
                    elif self.swarm[player].reached_goal(self.target_simulation):
                        reply["reward"] = 300
                        reply["score"] = self.get_score(player)
                    elif self.is_target_found():
                        reply["game_over"] = True
                        reply["reward"] = 1000
                        reply["score"] = self.get_score(player)
                        print("Game over due to target found")
                        self.reset_simulation()                        
                    elif self.swarm[player].location.distance_to(self.target_simulation) < RADIUS_TARGET:
                        reply["reward"] = 20
                        reply["score"] = self.get_score(player)
                    else:
                        reply["reward"] = 5
                        reply["score"] = self.get_score(player)

                    print("Sending : ", reply, "to player", player)
                    
                conn.sendall(json.dumps(reply).encode())
            except:
                break

        print("Lost connection")
        conn.close()

if __name__ == "__main__":
    simulation = Simulation()

    server = "localhost"
    port = 8080

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((server, port))
    except socket.error as e:
        str(e)

    s.listen(3)
    print("Server Started. Connect three clients to start the simulation")

    currentPlayer = 0
    while currentPlayer < 3:
        conn, addr = s.accept()
        print("Connected to:", addr)

        start_new_thread(simulation.connect_controller, (conn, currentPlayer))
        currentPlayer += 1


    simulation.running = True
    while simulation.running:
        simulation.clock.tick(FREQUENCY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        simulation.update_ui()


