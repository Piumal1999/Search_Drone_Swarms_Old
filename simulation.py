import pygame
from constants import *
from utils import *
from grid import GridField
from vehicle import Vehicle
import csv

vec2 = pygame.math.Vector2


class ScreenSimulation(object):
    '''
        Class responsable to represent the canvas variables
    '''

    def __init__(self):
        pygame.init()
        self.font16 = pygame.font.SysFont(None, 16)
        self.font20 = pygame.font.SysFont(None, 20)
        self.font24 = pygame.font.SysFont(None, 24)
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)


class Simulation(object):

    def __init__(self, screenSimulation):
        self.screenSimulation = screenSimulation
        self.score = 0

        # npc target
        self.npc = Npc_target()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.npc)

        self.target_simulation = None

        # Grid
        self.grid_field = GridField(RESOLUTION)

        # variables for swarm
        self.swarm = []
        self.create_swarm_uav(3)  # 3 drones hardcoded

        with open('obs.csv', 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, val in enumerate(row):
                    if val == 'X':
                        self.target_simulation = self.grid_field.get_cell_center([j, i])

    def create_swarm_uav(self, num_swarm):
        # get spawn location x,y from obs.csv (find + mark)
        with open('obs.csv', 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, val in enumerate(row):
                    if val == '+':
                        x, y = self.grid_field.get_cell_center([j, i])

        # Create N simultaneous Drones
        for d in range(0, num_swarm):
            drone = Vehicle(x, y, self.screenSimulation.screen)
            self.swarm.append(drone)

    def set_target(self, target):
        '''
            Sets target for all drones
        '''
        self.target_simulation = target
        for _ in self.swarm:
            _.set_mission_target(target)

    def draw_target(self):
        # draw target - npc
        if self.target_simulation:
            self.all_sprites.draw(self.screenSimulation.screen)
            self.all_sprites.update(self.target_simulation, 0)
            pygame.draw.circle(self.screenSimulation.screen,
                               LIGHT_BLUE, self.target_simulation, RADIUS_TARGET, 2)

    def draw(self):
        # draw grid of visited celss
        self.grid_field.draw(self.screenSimulation.screen)

        # draw target - npc
        self.draw_target()

    def run_simulation(self):
        # draw grid of visited cels, target and obstacles
        self.draw()

        # for every drone, it will update the collision avoidace, aling the direction and draw current position in simuation
        # self.rate.in_algorithms[self.rate.current_repetition].scan(
        #     self, self.list_obst) SPECIAL

        for drone in self.swarm:
            drone.draw(self.screenSimulation.screen)

            p = drone.get_position()
            col = int(p.x/RESOLUTION)
            row = int(p.y/RESOLUTION)

            # changes states of cell to visited
            self.grid_field.change_state_cell((col, row))
            drone.set_position_in_grid(col, row)

        # check completition of simulation
        if self.completed_simulation() >= 0.8:
            self.reset_simulation()

        return True

    def completed_simulation(self):
        count_completed = 0

        if self.target_simulation:
            for _ in self.swarm:
                if _.reached_goal(self.target_simulation):
                    count_completed = count_completed + 1
        return count_completed/3

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # wasd for drone control swarm[0], 1, 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.swarm[0].move_up()
                if event.key == pygame.K_s:
                    self.swarm[0].move_down()
                if event.key == pygame.K_a:
                    self.swarm[0].move_left()
                if event.key == pygame.K_d:
                    self.swarm[0].move_right()

                if event.key == pygame.K_UP:
                    self.swarm[1].move_up()
                if event.key == pygame.K_DOWN:
                    self.swarm[1].move_down()
                if event.key == pygame.K_LEFT:
                    self.swarm[1].move_left()
                if event.key == pygame.K_RIGHT:
                    self.swarm[1].move_right()

                if event.key == pygame.K_i:
                    self.swarm[2].move_up()
                if event.key == pygame.K_k:
                    self.swarm[2].move_down()
                if event.key == pygame.K_j:
                    self.swarm[2].move_left()
                if event.key == pygame.K_l:
                    self.swarm[2].move_right()

        game_over=False
        # if collision
        if self.is_collision():
            game_over=True

        return game_over, self.score

    def is_collision(self):
        """
            Checks if drone is colliding with another drone or with the limits of the screen or with an obstacle cell
            do not use functions from vehicle.py
        """
        for _ in self.swarm:
            # for __ in self.swarm:
            #     if _ != __:
            #         if _.location == __.location:
            #             return True

            if _.location.x < 0 or _.location.x > SCREEN_WIDTH or _.location.y < 0 or _.location.y > SCREEN_HEIGHT:
                return True

            # check if cell is obstacle
            if self.grid_field.get_state_cell(_.get_position_in_grid()) == 2:
                return True

        return False
    
    def reset_simulation(self):
        if self.swarm:
            for _ in self.swarm:
                _.set_mission_target(None)
                del _

        self.target_simulation = None

        # reset grid
        self.grid_field = GridField(RESOLUTION)

        # variables for swarm
        self.swarm = []
        self.create_swarm_uav(3)

        # get target from obs.csv
        target = None
        with open('obs.csv', 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, val in enumerate(row):
                    if val == 'X':
                        target = self.grid_field.get_cell_center([j, i])

        self.set_target(target)
