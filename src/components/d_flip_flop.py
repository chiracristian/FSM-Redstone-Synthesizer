#!/bin/python3

from blocks import *
from block_grid import BlockGrid
from components.d_latch import DLatch

D_FLIP_FLOP_WIDTH = 6
D_FLIP_FLOP_HEIGHT = 3
D_FLIP_FLOP_DEPTH = 4

class DFlipFlop(BlockGrid):
    def __init__(self):
        super().__init__(D_FLIP_FLOP_WIDTH, D_FLIP_FLOP_HEIGHT, D_FLIP_FLOP_DEPTH)

        # Place base plate
        for x in range (1, 4):
            for z in range(0, 2):
                self.blocks[x][0][z] = Block(BASE_SEQUENTIAL)
        
        # Place the base of output pin
        self.blocks[4][0][0] = Block(BASE_SEQUENTIAL)
        self.blocks[5][0][0] = Block(BASE_SEQUENTIAL)

        # Place output comparator and repeater
        self.blocks[4][1][0] = Comparator(Directions.WEST)
        self.blocks[5][1][0] = Repeater(Directions.WEST)

        # Place the flip flop components
        self.blocks[3][1][0] = Dropper(Directions.SOUTH, True)
        self.blocks[3][1][1] = Dropper(Directions.NORTH, False)

        self.blocks[2][1][0] = Torch(TorchType.WALL, Directions.EAST)
        self.blocks[2][1][1] = Repeater(Directions.WEST)

        self.blocks[1][1][0] = Block(BASE_SEQUENTIAL)
        self.blocks[1][1][1] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST)

        # Place a D latch in front
        self.paste(DLatch(), 0, 0, 0)