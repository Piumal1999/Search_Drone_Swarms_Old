from constants import *
import pygame as pg
from math import atan2, pi, exp, floor
import random
import copy 
import numpy as np
vec = pg.math.Vector2 

class GridField(object):
    def __init__(self, resolution):

        self.cols =int(SCREEN_WIDTH/resolution)  # Columns of the grid
        self.rows = int(SCREEN_HEIGHT/resolution)  # Rows of the grid
        self.resolution = resolution # Resolution of grid relative to window width and height in pixels

        self.field = [[vec(random.uniform(0,1),random.uniform(0,1)) for col in range(self.cols)] for row in range(self.rows)] # create matrix 
        self.cells = {}
        self.create_grid_cells()

    def create_grid_cells(self):
        blockSize =  self.resolution
        for x in range(0, SCREEN_WIDTH,  blockSize):
            for y in range(0, SCREEN_HEIGHT,  blockSize):
                self.cells[f'{int(x/blockSize)},{int(y/blockSize)}'] = Cell(vec(x,y), blockSize)

    def draw(self, screen):

        blockSize = self.resolution #Set the size of the grid block

        for x in range(0, SCREEN_WIDTH, blockSize):
            for y in range(0, SCREEN_HEIGHT, blockSize):
                rect = pg.Rect(x, y, blockSize, blockSize)
                pg.draw.rect(screen, (120,120,120), rect, 1)
                self.cells[f'{int(x/blockSize)},{int(y/blockSize)}'].draw_center(screen)

    def change_state_cell(self, cell):
        '''
            Cell is visitated
        '''
        self.cells[f'{cell[0]},{cell[1]}'].change_state()

    def get_state_cell(self, cell):
        '''
            Get if cell was visisted before
            cell: tuple with coordenates
            return: state of the cell 
        '''
        return self.cells[f'{cell[0]},{cell[1]}'].state

class Cell():
    def __init__(self, pos, blockSize):
        self.size_block = blockSize
        self.position = pos
        self.state = False

    def draw_center(self,screen):
        
        if self.state == False:
            pg.draw.circle(screen, (255,0,0), vec(self.position[0]+ self.size_block/2, self.position[1]+ self.size_block/2), 3)
        else:
            pg.draw.circle(screen, (0,255,0), vec(self.position[0]+ self.size_block/2, self.position[1]+ self.size_block/2), 3)

    def change_state(self):
        self.state = True