#!/bin/python3

from blocks import *
from block_grid import BlockGrid

D_FLIP_FLOP_WIDTH = 2
D_FLIP_FLOP_HEIGHT = 3
D_FLIP_FLOP_DEPTH = 3

class DFlipFlop(BlockGrid):
    def __init__(self):
        super().__init__(D_FLIP_FLOP_WIDTH, D_FLIP_FLOP_HEIGHT, D_FLIP_FLOP_DEPTH)

        # Place base plate
        for x in range (0, 2):
            for z in range(0, 2):
                self.blocks[x][0][z] = Block(BASE_SEQUENTIAL)
        
        # Place input repeaters
        self.blocks[0][1][0] = Repeater(Directions.WEST)
        self.blocks[1][1][0] = Repeater(Directions.WEST, False, True)

        # Place clock repeaters
        self.blocks[0][1][1] = Repeater(Directions.SOUTH)
        self.blocks[1][1][1] = Repeater(Directions.SOUTH, True)

        # Place clock pin and torch
        self.blocks[0][1][2] = Block(BASE_CLK_IN_PIN)
        self.blocks[0][2][2] = Wire()
        self.blocks[1][1][2] = Torch(TorchType.WALL, Directions.EAST)
        