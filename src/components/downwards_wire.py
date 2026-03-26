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
from components.product_term import PRODUCT_TERM_HEIGHT

DOWNWARDS_OR_WIRE_WIDTH = 3
DOWNWARDS_OR_WIRE_DEPTH = 4

class DownwardsOrWire(BlockGrid):
    def __init__(self, gates_count: int):
        size_x = DOWNWARDS_OR_WIRE_WIDTH
        size_y = PRODUCT_TERM_HEIGHT * gates_count + 1
        size_z = DOWNWARDS_OR_WIRE_DEPTH
        base_block = Block(BASE_DOWNWARDS_OR)

        super().__init__(size_x, size_y, size_z)

        for i in range(gates_count):
            current_built_step = i
            from_top_idx = gates_count - 1 - i
            torch_y = PRODUCT_TERM_HEIGHT * from_top_idx + 1

            # Place the block and wire next to the torch
            self.blocks[2][torch_y - 1][0] = base_block
            if current_built_step != 0:
                self.blocks[2][torch_y][0] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH | WIRE_SIDE_WEST)
            else:
                self.blocks[2][torch_y][0] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

            # If at the bottom, place an output pin and stop
            if from_top_idx == 0:
                # Place 3 blocks in a line
                self.blocks[2][torch_y - 1][1] = base_block
                self.blocks[2][torch_y - 1][2] = base_block
                self.blocks[2][torch_y - 1][3] = base_block
                
                # Place two straight wires
                self.blocks[2][torch_y][1] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
                self.blocks[2][torch_y][2] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

                # Place the output repeater
                self.blocks[2][torch_y][3] = Repeater(Directions.NORTH)
                self.delay += 1
                break

            # Place the block one level down
            self.blocks[2][torch_y - 2][1] = base_block
            self.blocks[2][torch_y - 1][1] = Wire(WIRE_UP_NORTH | WIRE_SIDE_WEST)

            # Place the staircase blocks to the side
            self.blocks[1][torch_y - 3][1] = base_block
            self.blocks[1][torch_y - 4][0] = base_block

            # Put repeater at every 3rd step (except the first and last)
            is_not_first = current_built_step != 0
            is_not_last = from_top_idx != 1
            is_3rd_step = (current_built_step + 1) % 3 == 0

            if is_not_first and is_not_last and is_3rd_step:
                # Extend out the stair
                self.blocks[0][torch_y - 3][1] = base_block
                self.blocks[0][torch_y - 4][0] = base_block

                # Add the wires
                self.blocks[1][torch_y - 2][1] = Wire(WIRE_UP_EAST | WIRE_SIDE_WEST)
                self.blocks[0][torch_y - 2][1] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_EAST)
                self.blocks[0][torch_y - 3][0] = Wire(WIRE_UP_SOUTH | WIRE_SIDE_EAST)
                self.blocks[1][torch_y - 3][0] = Repeater(Directions.WEST)
                self.delay += 1

            # Otherwise just put wires
            else:
                self.blocks[1][torch_y - 2][1] = Wire(WIRE_SIDE_NORTH | WIRE_UP_EAST)
                self.blocks[1][torch_y - 3][0] = Wire(WIRE_UP_SOUTH | WIRE_SIDE_EAST)
