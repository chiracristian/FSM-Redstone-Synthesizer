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
from logic.sop_expression import ProductTerm, LiteralState

PRODUCT_TERM_HEIGHT = 3
PRODUCT_TERM_DEPTH = 5

PRODUCT_TERM_MAX_INPUTS = 14

class ProductTermGate(BlockGrid):
    base_block = Block(BASE_PRODUCT_TERM)

    def place_pin(self, current_x: int, literal: LiteralState):
        match literal:
            case LiteralState.ABSENT:
                pass
            
            case LiteralState.POSITIVE:
                # Place a torch and connect it to the rail
                self.blocks[current_x][1][2] = self.base_block
                self.blocks[current_x][2][2] = Torch(TorchType.FLOOR)
                self.blocks[current_x][2][3].north_connection = WireConnection.SIDE
                self.rail_torches_pos.append((current_x, 2, 2))

                # Place the connection, one level lower
                self.blocks[current_x][0][1] = self.base_block
                self.blocks[current_x][0][0] = self.base_block

                self.blocks[current_x][1][1] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
                self.blocks[current_x][1][0] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

            case LiteralState.NEGATED:
                # Place a wire in the upper part
                self.blocks[current_x][1][2] = self.base_block
                self.blocks[current_x][2][2] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
                self.blocks[current_x][2][3].north_connection = WireConnection.SIDE

                # Place the connection, one level lower, with a repeater
                self.blocks[current_x][0][1] = self.base_block
                self.blocks[current_x][0][0] = self.base_block
                self.blocks[current_x][1][1] = Repeater(Directions.NORTH)

                self.blocks[current_x][1][0] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

    def __init__(self, term: ProductTerm):
        self.inputs_count = len(term.inputs)
        self.state_vars_count = len(term.states)

        self.pins_count = self.inputs_count + self.state_vars_count

        size_x = 2 * self.pins_count - 1
        size_y = PRODUCT_TERM_HEIGHT
        size_z = PRODUCT_TERM_DEPTH
        super().__init__(size_x, size_y, size_z)

        # Put the output rail
        for x in range(0, size_x):
            self.blocks[x][1][3] = self.base_block
            self.blocks[x][2][3] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST)
            if x == 0:
                self.blocks[x][2][3].west_connection = WireConnection.NONE
            if x == size_x - 1:
                self.blocks[x][2][3].east_connection = WireConnection.NONE

        self.rail_torches_pos: list[tuple[int, int, int]] = []

        # Now put the input variables pins
        current_x = size_x - 1
        for input_var in term.inputs:
            self.place_pin(current_x, input_var)
            current_x -= 2

        # And same for the state variables
        for state_var in term.states:
            self.place_pin(current_x, state_var)
            current_x -= 2

        # Propagate the signals from the torches
        for pos in self.rail_torches_pos:
            self.propagate_power_from_torch(pos[0], pos[1], pos[2])

        # Put the output torch
        self.out_torch_x = size_x // 2
        self.blocks[self.out_torch_x][1][4] = Torch(TorchType.WALL, Directions.SOUTH)

        # Turn off the torch if the output rail is energized
        if (self.blocks[self.out_torch_x][2][3].is_energized()):
            self.blocks[self.out_torch_x][1][4].lit = False
        else:
            self.torches_pos.append((self.out_torch_x, 1, 4))

        # The delay is 2 (1 for input pins, 1 for the output torch)
        self.delay = 2
