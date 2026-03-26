# FSM-Redstone-Synthesizer
# Copyright (C) 2025-2026  Cristian-Ioan-George Chira (github.com/chiracristian)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free-Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from blocks import *
from block_grid import BlockGrid

FEEDBACK_WIRE_HEIGHT = 4

# This is meant to be pasted right at the input
class FeedbackWire(BlockGrid):
    def __init__(self, front_wire_length: int, side_wire_length: int, back_wire_length: int,
                    output_pin_length: int):
        base_block = Block(BASE_STATE_VAR_FEEDBACK)
        
        size_x = front_wire_length + 2
        size_y = FEEDBACK_WIRE_HEIGHT
        size_z = side_wire_length + 2
        super().__init__(size_x, size_y, size_z)

        # Place the stair into the D flip flop
        self.blocks[0][0][1] = base_block
        self.blocks[0][1][1] = Wire(WIRE_UP_NORTH | WIRE_SIDE_EAST)

        self.blocks[0][1][0] = base_block
        self.blocks[0][2][0] = Wire(WIRE_SIDE_SOUTH | WIRE_UP_EAST)

        # Place the line parallel to the inputs
        for x in range(1, size_x - 1):
            self.blocks[x][2][0] = base_block
            self.blocks[x][3][0] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST)

        # Place the first turn
        self.blocks[size_x - 1][2][0] = base_block
        self.blocks[size_x - 1][3][0] = Wire(WIRE_SIDE_WEST | WIRE_SIDE_SOUTH)

        # Place the line parallel to the towers
        for z in range(1, size_z - 1):
            self.blocks[size_x - 1][2][z] = base_block
            self.blocks[size_x - 1][3][z] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

        # Place the second turn
        self.blocks[size_x - 1][2][size_z - 1] = base_block
        self.blocks[size_x - 1][3][size_z - 1] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_WEST)

        # Place the back wire
        x = size_x - 2
        for _ in range(0, back_wire_length):
            self.blocks[x][2][size_z - 1] = base_block
            self.blocks[x][3][size_z - 1] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST)
            x -= 1

        # Place the stairs to the level of the output pin
        self.blocks[x][1][size_z - 1] = base_block
        self.blocks[x][2][size_z - 1] = Wire(WIRE_UP_EAST | WIRE_SIDE_WEST)
        x -= 1

        self.blocks[x][0][size_z - 1] = base_block
        if output_pin_length == 0:
            self.blocks[x][1][size_z - 1] = Wire(WIRE_UP_EAST | WIRE_SIDE_WEST)
        else:
            self.blocks[x][1][size_z - 1] = Wire(WIRE_UP_EAST | WIRE_SIDE_NORTH)

        # Place the connection to the output pin
        z = size_z - 2
        for _ in range(0, output_pin_length):
            self.blocks[x][0][z] = base_block
            self.blocks[x][1][z] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
            z -= 1

        # Place repeaters
        current_power = MAX_WIRE_POWER
        start_z = z + 1

        # Place repeaters along the output pin
        for i in range(0, output_pin_length):
            if current_power == 0 or (i == output_pin_length - 1 and current_power <= 3):
                self.blocks[x][1][start_z + i] = Repeater(Directions.NORTH)
                self.delay += 1
                current_power = MAX_WIRE_POWER + 1

            current_power -= 1

        # Decrease the power for the stairs
        current_power -= 2

        # Place repeaters along the back line
        start_x = x + 2
        for x in range(start_x, start_x + back_wire_length):
            if current_power == 0 or (x == size_x - 1 and current_power <= 1):
                self.blocks[x][3][size_z - 1] = Repeater(Directions.WEST)
                self.delay += 1
                current_power = MAX_WIRE_POWER + 1

            current_power -= 1

        # Decrease the power for the corner
        current_power -= 1

        # Place repeaters along the line parallel with the towers
        for z in range(size_z - 2, 0, -1):
            if current_power == 0 or (z == 1 and current_power <= 1):
                self.blocks[size_x - 1][3][z] = Repeater(Directions.SOUTH)
                self.delay += 1
                current_power = MAX_WIRE_POWER + 1

            current_power -= 1

        # Decrease power for the corner
        current_power -= 1

        # Place repeaters along the line parallel to the inputs
        for x in range(size_x - 2, 0, -1):
            if current_power == 0 or (x == 2 and current_power <= 3):
                self.blocks[x][3][0] = Repeater(Directions.EAST)
                self.delay += 1
                current_power = MAX_WIRE_POWER + 1

            current_power -= 1
