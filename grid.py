from constants import *
import pygame as pg
import csv
import numpy as np
# importing "heapq" to implement heap queue
import heapq
import random


vec = pg.math.Vector2


DEFAULT = 0
OBSTACLE = 1


class GridField(object):
    def __init__(self, resolution):

        self.cols = int(SCREEN_WIDTH/resolution)  # Columns of the grid
        self.rows = int(SCREEN_HEIGHT/resolution)  # Rows of the grid
        # grid memory using numpy array
        self.cells = np.ndarray((self.rows+1, self.cols+1), dtype=Cell)
        # Resolution of grid relative to window width and height in pixels
        self.resolution = resolution
        # print(f' Grid created with  col:{self.cols} row:{self.rows}')
        # self.field = [[vec(random.uniform(0,1),random.uniform(0,1)) for col in range(self.cols)] for row in range(self.rows)] # create matrix
        self.cells_ = {}  # Memory using dictionary NOT USED
        self.h_cells = []
        heapq.heapify(self.h_cells)

        self.create_grid_cells()

    def create_grid_cells(self):
        '''
            Creates grid with cells according to resolution 
        '''
        blockSize = self.resolution
        for x in range(0, SCREEN_WIDTH,  blockSize):
            for y in range(0, SCREEN_HEIGHT,  blockSize):
                # self.cells_[f'{int(x/blockSize)},{int(y/blockSize)}'] = Cell(vec(x,y), blockSize)
                #             row                  col
                self.cells[int(y/blockSize)][int(x/blockSize)] = Cell(vec(x, y), blockSize)
                # priority queue HEAP
                heapq.heappush(self.h_cells,  (self.cells[int(y/blockSize)][int(x/blockSize)].state, (int(y/blockSize), int(x/blockSize))))

        with open('obs.csv', 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                for j, val in enumerate(row):
                    if val == '1':
                        self.cells[i][j].state = OBSTACLE

    def draw(self, screen):

        blockSize = self.resolution  # Set the size of the grid block

        for x in range(0, SCREEN_WIDTH, blockSize):
            for y in range(0, SCREEN_HEIGHT, blockSize):
                rect = pg.Rect(x, y, blockSize, blockSize)
                # if obstacle, fill black
                if self.cells[int(y/blockSize)][int(x/blockSize)].state == OBSTACLE:
                    pg.draw.rect(screen, BLACK, rect)
                else:
                    pg.draw.rect(screen, (120, 120, 120), rect, 1)

    def get_size(self):
        '''
            Returns a tuple containing sizeof the grid :(#col,#row) 
        '''
        return (self.cols, self.rows)

    def get_cell_center(self, cell):
        return self.cells[cell[1]][cell[0]].get_cell_center()

    def get_cell_when_xy_is_given(self, x, y):
        try:
            return self.cells[int(y/self.resolution)][int(x/self.resolution)]
        except:
            return None

    def get_cell_center_when_xy_is_given(self, x, y):
        return self.get_cell_when_xy_is_given(x, y).get_cell_center()
    
    def get_random_cell_center(self):
        '''
            This method will return a random cell center
        '''
        return self.cells[random.randint(0, self.rows)][random.randint(0, self.cols)].get_cell_center()


class Cell():
    '''
        Represents a cell in the grid
        Every cell represents an area in the map that is being searched
    '''

    def __init__(self, pos, blockSize):
        self.size_block = blockSize
        self.position = pos
        self.state = DEFAULT
        self.center_in_coord_global = vec(
            self.position[0] + self.size_block/2, self.position[1] + self.size_block/2)

    def change_state(self, state=DEFAULT):
        if self.state != OBSTACLE:
            self.state = state

    def get_cell_center(self):
        return self.center_in_coord_global
