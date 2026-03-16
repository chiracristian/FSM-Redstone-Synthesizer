#!/bin/python3

from blocks import *
from block_grid import BlockGrid

CLOCK_BUS_HEIGHT = 2

class ClockBus(BlockGrid):
    def __init__(self, flip_flop_count: int, required_delay: int):
        base_block = Block(BASE_SEQUENTIAL)
        tree_length = 3 * (flip_flop_count - 1) + 1

        size_x = tree_length
        size_y = CLOCK_BUS_HEIGHT

        clock_part_repeater_count = required_delay // 4 + (1 if required_delay % 4 != 0 else 0)
        clock_part_z = clock_part_repeater_count + 3
        size_z = tree_length + 1 + clock_part_z

        super().__init__(size_x, size_y, size_z)

        # Build the connections to the clock pins
        current_bus_power = MAX_WIRE_POWER
        for x in range(0, size_x):
            self.blocks[x][0][tree_length] = base_block

            # Place a repeated if power gets low
            if current_bus_power == 1:
                self.blocks[x][1][tree_length] = Repeater(Directions.WEST)
                current_bus_power = MAX_WIRE_POWER
                continue

            # Place a line to a D flip flop every 3 blocks
            if x % 3 == 0:
                if x == 0:
                    self.blocks[x][1][tree_length] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
                elif x == size_x - 1:
                    self.blocks[x][1][tree_length] = Wire(WIRE_SIDE_WEST | WIRE_SIDE_NORTH)
                else:
                    self.blocks[x][1][tree_length] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST | WIRE_SIDE_NORTH)

                current_line_power = current_bus_power - 1
                for z in range(tree_length - 1, x - 1, -1):
                    self.blocks[x][0][z] = base_block
                    if current_line_power == 0:
                        self.blocks[x][1][z] = Repeater(Directions.SOUTH)
                        current_line_power = MAX_WIRE_POWER + 1
                    else:
                        self.blocks[x][1][z] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

                    current_line_power -= 1
            else:
                self.blocks[x][1][tree_length] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST)

            current_bus_power -= 1

        # Place the interconnection between the tree and the clock
        self.blocks[0][0][tree_length + 1] = base_block
        self.blocks[0][1][tree_length + 1] = Repeater(Directions.SOUTH)

        # Place the clock plate
        for x in range(0, 2):
            for z in range(tree_length + 2, size_z):
                self.blocks[x][0][z] = Block(BASE_SEQUENTIAL)

        # Place the wires on the clock part
        self.blocks[0][1][tree_length + 2] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH | WIRE_SIDE_EAST)
        self.blocks[1][1][tree_length + 2] = Wire(WIRE_SIDE_SOUTH | WIRE_SIDE_WEST)
        for z in range(tree_length + 3, size_z - 1):
            self.blocks[0][1][z] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
        self.blocks[1][1][size_z - 1] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_WEST)

        # Place the comparator from where the clock will be powered
        self.blocks[0][1][size_z - 1] = Comparator(Directions.SOUTH, ComparatorModes.SUBTRACT)

        # Place the repeaters generating the required period of the clock
        for z in range(tree_length + 3, size_z - 2):
            self.blocks[1][1][z] = Repeater(Directions.NORTH, False, False, 4)
        if required_delay % 4 != 0:
            self.blocks[1][1][size_z - 2] = Repeater(Directions.NORTH, False, False, required_delay % 4)
        else:
            self.blocks[1][1][size_z - 2] = Repeater(Directions.NORTH, False, False, 4)
