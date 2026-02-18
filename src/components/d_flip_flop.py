#!/bin/python3

from blocks import *
from block_grid import BlockGrid

D_FLIP_FLOP_SIZE_X = 6
D_FLIP_FLOP_SIZE_Y = 3
D_FLIP_FLOP_SIZE_Z = 4
class DFlipFlop(BlockGrid):
    def __init__(self):
        super().__init__(D_FLIP_FLOP_SIZE_X, D_FLIP_FLOP_SIZE_Y, D_FLIP_FLOP_SIZE_Z)

        # Place base plate
        for x in range (0, 4):
            for z in range(2, 4):
                self.blocks[x][0][z] = Block(BASE_SEQUENTIAL)
        
        self.blocks[4][0][3] = Block(BASE_SEQUENTIAL)
        self.blocks[5][0][3] = Block(BASE_SEQUENTIAL)

        # Place the D input repeater
        self.blocks[0][1][3] = Repeater(Directions.WEST, False, True)

        # Place the logic in-between
        self.blocks[1][1][3] = Block(BASE_SEQUENTIAL)

        self.blocks[1][1][2] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST)

        self.blocks[2][1][3] = Torch(TorchType.WALL, Directions.EAST)
        self.blocks[2][1][2] = Repeater(Directions.WEST, False, False)

        # Place the droppers
        self.blocks[3][1][3] = Dropper(Directions.NORTH, True)
        self.blocks[3][1][2] = Dropper(Directions.SOUTH, False)

        # Place the output
        self.blocks[4][1][3] = Comparator(Directions.WEST)
        self.blocks[5][1][3] = Repeater(Directions.WEST, False)

        # Place the clock pin
        self.blocks[0][1][2] = Repeater(Directions.NORTH, True)
        self.blocks[0][1][1] = Torch(TorchType.WALL, Directions.SOUTH)
        self.blocks[0][1][0] = Block(BASE_SEQUENTIAL_CLK_PIN)
        self.blocks[0][2][0] = Wire()
