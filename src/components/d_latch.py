#!/bin/python3

from blocks import *
from block_grid import BlockGrid

D_LATCH_WIDTH = 1
D_LATCH_HEIGHT = 3
D_LATCH_DEPTH = 4

class DLatch(BlockGrid):
    def __init__(self):
        super().__init__(D_LATCH_WIDTH, D_LATCH_HEIGHT, D_LATCH_DEPTH)

        # Place the base plate
        self.blocks[0][0][0] = Block(BASE_SEQUENTIAL)
        self.blocks[0][0][1] = Block(BASE_SEQUENTIAL)

        # Place the repeaters
        self.blocks[0][1][0] = Repeater(Directions.WEST, False, True)
        self.blocks[0][1][1] = Repeater(Directions.SOUTH, True)

        # Place the CLK pin
        self.blocks[0][1][2] = Torch(TorchType.WALL, Directions.NORTH)
        self.blocks[0][1][3] = Block(BASE_CLK_IN_PIN)
        self.blocks[0][2][3] = Wire(WIRE_SIDE_EAST | WIRE_UP_WEST)
