import pygame
from constants import *
from utils import *
from grid import GridField
from vehicle import Vehicle
import csv

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

            p = drone.get_position()
            col = int(p.x/RESOLUTION)
            row = int(p.y/RESOLUTION)

            # changes states of cell to visited
            self.grid_field.change_state_cell((col, row))

        pygame.display.flip()

    def play_step(self, action=None):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if action is None:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        action = [1,0,0,0]
                    elif event.key == pygame.K_DOWN:
                        action = [0,1,0,0]
                    elif event.key == pygame.K_LEFT:
                        action = [0,0,1,0]
                    elif event.key == pygame.K_RIGHT:
                        action = [0,0,0,1]

        self.swarm[0].move(action)

        game_over=False

        # if collision
        if self.is_collision():
            game_over=True

        # if drone 0 reach target game over
        if self.swarm[0].reached_goal(self.target_simulation):
            game_over=True
        
        self.update_ui()

        return game_over

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
            if cell.state == 2:
                return True

        return False
    
if __name__ == "__main__":
    simulation = Simulation()

    run = True
    while True:
        gameover = simulation.play_step(None)
        if gameover:
            simulation.reset_simulation()

