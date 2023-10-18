import pygame as pg
from utils import Aircraft, random_color
from constants import *

vec2 = pg.math.Vector2


class Vehicle(object):

    def __init__(self, x, y, window):
        """
            idealized vehicle representing a drone

            :param x and y: represents initial position
            :param window: pygame screen were it will be draw
        """

        # Variables used to move drone
        self.location = vec2(x, y)  # Position in screen

        self.radius = SIZE_DRONE  # Drone Size

        self.memory_locations = []  # To draw track
        self.memory_locations.append((self.location.x, self.location.y))

        # Picks a random color for target, is used to differentiate visually during simulation
        self.color_target = random_color()

        self.window = window  # Screen where the simulation is happening

        # Variables to draw drone using Sprites
        self.drone = Aircraft()
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.drone)

    def move(self, action):
        """
            Moves drone in a direction
        """
        if action == [1, 0, 0, 0]:
            self.location.y -= STEP_SIZE
        elif action == [0, 1, 0, 0]:
            self.location.y += STEP_SIZE
        elif action == [0, 0, 1, 0]:
            self.location.x -= STEP_SIZE
        elif action == [0, 0, 0, 1]:
            self.location.x += STEP_SIZE
        self.update()

    def reached_goal(self, target):
        return target and (target - self.location).length() <= RADIUS_TARGET

    def update(self):
        """
            Update drone position memory
        """
        self.memory_locations.append((self.location.x, self.location.y))

    def get_position(self):
        return self.location

    def draw(self, window):
        """
            Defines shape of vehicle and draw it to screen
        """

        # draws track
        if len(self.memory_locations) >= 2:
            pg.draw.lines(self.window, self.color_target, False, self.memory_locations, 1)

        # Draw search radius
        pg.draw.circle(window, RED, self.location, RADIUS_TARGET, 1)

        # Use sprite to draw drone
        self.all_sprites.draw(self.window)
        self.all_sprites.update(self.location, 0)

    def get_travelled_distance(self):
        distance = 0
        for i in range(len(self.memory_locations)-1):
            distance += vec2(self.memory_locations[i]).distance_to(vec2(self.memory_locations[i+1]))
        return distance

    # Deleting (Calling destructor)
    # def __del__(self):
        # print('Drone Deleted')
