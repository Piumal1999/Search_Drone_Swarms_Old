# Simulation Parameters
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
PIX2M = 0.01  # factor to convert from pixels to meters
M2PIX = 100.0  # factor to convert from meters to pixels
SIZE_DRONE = 18
RESOLUTION = 50 # Of grid
STEP_SIZE = 50 # step of drone
RADIUS_OBSTACLES = 40
TIME_MAX_SIMULATION = 60 # Time to stop simulation in case the conditions are not completed

# Sample Time Parameters
FREQUENCY = 60.0  # simulation frequency
SAMPLE_TIME = 1.0 / FREQUENCY  # simulation sample time

# Behavior Parameters
RADIUS_TARGET = 450
COMMUNICATION_DISTANCE = 25 # distance to communicate

# Colors
BLACK = (0,0,0)
LIGHT_BLUE = (224, 255, 255)
BLUE = (0,0,255)
RED = (255,0,0)