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

        self.moves = 0  # Number of moves done by drone
        self.score = 0  # Score of drone

        # Variables used to move drone
        self.location = vec2(x, y)  # Position in screen

        self.radius = SIZE_DRONE  # Drone Size

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
        if action == "W":
            self.location.y -= STEP_SIZE
        elif action == "S":
            self.location.y += STEP_SIZE
        elif action == "A":
            self.location.x -= STEP_SIZE
        elif action == "D":
            self.location.x += STEP_SIZE
        elif action == "0":
            pass

    def reached_goal(self, target):
        return target and (target - self.location).length() < 100

    def get_position(self):
        return self.location
    
    def get_distance_to(self, target):
        return (target - self.location).length()

    def draw(self, window):
        """
            Defines shape of vehicle and draw it to screen
        """

        # Draw communication radius
        pg.draw.circle(window, RED, self.location, COMMUNICATION_DISTANCE, 1)

        # Use sprite to draw drone
        self.all_sprites.draw(self.window)
        self.all_sprites.update(self.location, 0)

    # Deleting (Calling destructor)
    # def __del__(self):
        # print('Drone Deleted')
