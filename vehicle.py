import pygame as pg
from utils import Aircraft, random_color
from constants import *

# directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

vec2 = pg.math.Vector2


class Vehicle(object):

    def __init__(self, x, y, window):
        """
            idealized vehicle representing a drone

            :param x and y: represents initial target
            :param window: pygame screen were it will be draw
        """

        self.debug = False  # debug lines is Off

        # Variables used to move drone
        self.location = vec2(x, y)  # Position in screen
        self.mission_target = vec2(x, y)

        self.radius = SIZE_DRONE  # Drone Size
        self.desired = vec2()
        # closest drone
        self.closest_drone = None
        self.index_closest_drone = None

        self.memory_locations = []  # To draw track
        self.memory_locations.append((self.location.x, self.location.y))

        # Picks a random color for target, is used to differentiate visually during simulation
        self.color_target = random_color()

        self.window = window  # Screen where the simulation is happening

        # Variables to draw drone using Sprites
        self.drone = Aircraft()
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.drone)

        # variables to search in grid
        self.position_in_grid = (0, 0)

    def reached_goal(self, target):
        return target and (target - self.location).length() <= RADIUS_TARGET

    def update(self):
        """
            Update drone position memory
        """
        self.memory_locations.append((self.location.x, self.location.y))

    def move(self, direction):
        """
            Moves drone in a direction
        """
        if direction == UP:
            self.location.y -= STEP_SIZE
        elif direction == DOWN:
            self.location.y += STEP_SIZE
        elif direction == LEFT:
            self.location.x -= STEP_SIZE
        elif direction == RIGHT:
            self.location.x += STEP_SIZE
        self.update()

    def move_up(self):
        self.move(UP)

    def move_down(self):
        self.move(DOWN)

    def move_left(self):
        self.move(LEFT)

    def move_right(self):
        self.move(RIGHT)

    def mission_accomplished(self):
        if self.mission_target:
            return self.location.x == self.mission_target.x and self.location.y == self.mission_target.y
        else:
            return False

    def get_position(self):
        return self.location

    def set_mission_target(self, target):
        self.mission_target = target

    def get_mission_target(self):
        try:
            return self.mission_target
        except:
            return None

    def draw(self, window):
        """
            Defines shape of vehicle and draw it to screen
        """
        # if self.closest_drone:
        #     pg.draw.line(self.window, self.color_target,
        #                  self.location, self.closest_drone, 1)

        # draws track
        if len(self.memory_locations) >= 2:
            pg.draw.lines(self.window, self.color_target,
                          False, self.memory_locations, 1)

        # Draw communication range circle
        pg.draw.circle(window, (0, 255, 0), self.location,
                       COMMUNICATION_DISTANCE, 1)

        # Draw search radius
        pg.draw.circle(window, RED, self.location, RADIUS_TARGET, 1)

        # Use sprite to draw drone
        self.all_sprites.draw(self.window)
        self.all_sprites.update(self.location, 0)

    def get_closest_drone(self):
        return self.closest_drone

    def set_position_in_grid(self, x, y):
        self.position_in_grid = (x, y)

    def get_position_in_grid(self):
        return self.position_in_grid

    def get_travelled_distance(self):
        distance = 0
        for i in range(len(self.memory_locations)-1):
            distance += vec2(self.memory_locations[i]).distance_to(
                vec2(self.memory_locations[i+1]))
        return distance

    # Deleting (Calling destructor)
    # def __del__(self):
        # print('Drone Deleted')
