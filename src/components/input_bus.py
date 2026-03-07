#!/bin/python3

from blocks import *
from block_grid import BlockGrid
from components.sum_tower import SumTower, TOWERS_SPACING

INPUT_BUS_HEIGHT = 4

class InputBus(BlockGrid):
    def __init__(self, base_block: Block, towers_count: int, tower_width: int,
                 pin_idx: int, pin_connection_length: int, additional_extend_length: int):
        size_x = towers_count * tower_width + \
                (towers_count - 1) * TOWERS_SPACING + additional_extend_length
        size_y = INPUT_BUS_HEIGHT
        size_z = pin_connection_length + 1
        
        super().__init__(size_x, size_y, size_z)

        junctions_x: list[int] = []

        # Place connection pins
        current_x = size_x - 1 - 2 * pin_idx
        for tower_idx in range(0, towers_count):
            # Place the junction
            junctions_x.append(current_x)
            self.blocks[current_x][1][0] = base_block
            if tower_idx == 0:
                self.blocks[current_x][2][0] = Wire(WIRE_SIDE_SOUTH | WIRE_UP_WEST)
            else:
                self.blocks[current_x][2][0] = Wire(WIRE_SIDE_SOUTH | WIRE_UP_EAST | WIRE_UP_WEST)

            # Place the pin
            self.blocks[current_x][0][1] = base_block
            self.blocks[current_x][1][1] = Wire(WIRE_UP_NORTH | WIRE_SIDE_SOUTH)
            for z in range(2, size_z):
                self.blocks[current_x][0][z] = base_block
                self.blocks[current_x][1][z] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
            current_x -= tower_width + TOWERS_SPACING

        # Place the bus rail
        next_junction_idx = 1
        for x in range(junctions_x[0] - 1, -1, -1):
            # Skip placing at the junctions
            if next_junction_idx < towers_count and x == junctions_x[next_junction_idx]:
                next_junction_idx += 1
                continue

            # Place the line
            self.blocks[x][2][0] = base_block
            self.blocks[x][3][0] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST)

        # Add repeaters
        max_delay = 0
        bus_delay = 0
        bus_power = MAX_WIRE_POWER
        next_junction_idx = towers_count

        for x in range(0, size_x):
            # Decrease the power
            bus_power -= 1

            # Go on the pin if it's junction
            if x == junctions_x[next_junction_idx - 1]:
                pin_power = bus_power
                pin_delay = bus_delay
                for z in range(1, size_z):
                    pin_power -= 1
                    if pin_power == 0:
                        self.blocks[x][1][z] = Repeater(Directions.NORTH)
                        pin_delay += 1
                        pin_power = MAX_WIRE_POWER + 1
                        max_delay = max(max_delay, pin_delay)

                next_junction_idx -= 1

            # Place a repeater if power reached 0
            # or if two blocks away from junction and power is 3 or less
            if (x == junctions_x[next_junction_idx - 1] - 2 and bus_power <= 3) \
            or bus_power == 0:
                self.blocks[x][3][0] = Repeater(Directions.WEST)
                bus_delay += 1
                bus_power = MAX_WIRE_POWER + 1
                max_delay = max(max_delay, bus_delay)

        self.delay = max_delay