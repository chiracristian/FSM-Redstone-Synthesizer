#!/bin/python3

from blocks import *
from block_grid import BlockGrid

UPWARDS_WIRE_WIDTH = 1
UPWARDS_WIRE_DEPTH = 6
EFFECTIVE_UPWARDS_WIRE_DEPTH = UPWARDS_WIRE_DEPTH - 2

class UpwardsWire(BlockGrid):
    def add_vertical_repeater(self, y: int, z: int, facing: Directions):
        # Do not add repeater if we would go out of bounds
        if self.is_out_of_bounds(0, y + 3, 0):
            return

        direction = 0
        torch_facing = Directions.INVALID
        match facing:
            case Directions.NORTH:
                direction = -1
                torch_facing = Directions.SOUTH
            case Directions.SOUTH:
                direction = 1
                torch_facing = Directions.NORTH
            case _:
                raise ValueError("Facing of the repeaters of UpwardsWire must be North or South")
            
        # Put the wire into the first torch
        self.blocks[0][y][z + direction] = Block(BASE_COMBINATIONAL_BOTTOM)
        self.blocks[0][y + 1][z + direction] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

        # Put the first inverter
        self.blocks[0][y + 1][z + 2 * direction] = Block(BASE_COMBINATIONAL_BOTTOM)
        self.blocks[0][y + 2][z + 2 * direction] = Torch(TorchType.FLOOR)

        # Put the second inverter
        self.blocks[0][y + 3][z + 2 * direction] = Block(BASE_COMBINATIONAL_BOTTOM)
        self.blocks[0][y + 3][z + direction] = Torch(TorchType.WALL, torch_facing, False)

    def __init__(self, height: int, facing: Directions):
        size_x = UPWARDS_WIRE_WIDTH
        size_y = height + 1
        size_z = UPWARDS_WIRE_DEPTH
        super().__init__(size_x, size_y, size_z)

        y_offset = 0
        match facing:
            case Directions.NORTH:
                pass
            case Directions.SOUTH:
                y_offset = -1
            case _:
                raise ValueError("Facing of the repeaters of UpwardsWire must be North or South")

        z = 0
        for y in range(0, height):
            repeater_y = y + y_offset

            # Put the glass with a wire on top
            if y % 2 == 0:
                z = 2
                self.blocks[0][y][z] = Block(BASE_COMBINATIONAL_TRANSPARENT)
                self.blocks[0][y + 1][z] = Wire(WIRE_SIDE_NORTH | WIRE_UP_SOUTH)
            else:
                z = 3
                self.blocks[0][y][z] = Block(BASE_COMBINATIONAL_TRANSPARENT)
                self.blocks[0][y + 1][z] = Wire(WIRE_UP_NORTH | WIRE_SIDE_SOUTH)

            # Every 10 blocks put a repeater
            if repeater_y % 10 == 0 and repeater_y != 0:
                self.add_vertical_repeater(y, z, facing)

        # The top wire is flat
        self.blocks[0][height][z] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
