#!/bin/python3

from blocks import *
from block_grid import BlockGrid
from logic.sop_expression import ProductTerm, LiteralState

class ProductTermGate(BlockGrid):
    def place_pin(self, current_x: int, literal: LiteralState):
        match literal:
            case LiteralState.ABSENT:
                pass
            
            case LiteralState.POSITIVE:
                # Place a torch
                self.blocks[current_x][1][2] = Block(BASE_COMBINATIONAL_BOTTOM)
                self.blocks[current_x][2][2] = Torch(TorchType.FLOOR)

                # Place the connection, one level lower
                self.blocks[current_x][0][1] = Block(BASE_COMBINATIONAL_BOTTOM)
                self.blocks[current_x][0][0] = Block(BASE_COMBINATIONAL_BOTTOM)

                self.blocks[current_x][1][1] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)
                self.blocks[current_x][1][0] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

            case LiteralState.NEGATED:
                # Place a wire in the upper part
                self.blocks[current_x][1][2] = Block(BASE_COMBINATIONAL_BOTTOM)
                self.blocks[current_x][2][2] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

                # Place the connection, one level lower, with a repeater
                self.blocks[current_x][0][1] = Block(BASE_COMBINATIONAL_BOTTOM)
                self.blocks[current_x][0][0] = Block(BASE_COMBINATIONAL_BOTTOM)
                self.blocks[current_x][1][1] = Repeater(Directions.NORTH)

                self.blocks[current_x][1][0] = Wire(WIRE_SIDE_NORTH | WIRE_SIDE_SOUTH)

    def __init__(self, term: ProductTerm):
        size_x = 2 * (len(term.inputs) + len(term.states)) - 1
        size_y = 3
        size_z = 5
        super().__init__(size_x, size_y, size_z)

        # Put the output torch
        out_torch_x = size_x // 2
        self.blocks[out_torch_x][1][4] = Torch(TorchType.WALL, Directions.SOUTH)

        # Put the output rail
        for x in range(0, size_x):
            self.blocks[x][1][3] = Block(BASE_COMBINATIONAL_BOTTOM)
            if x == 0:
                self.blocks[x][2][3] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_NORTH)
            elif x == size_x - 1:
                self.blocks[x][2][3] = Wire(WIRE_SIDE_WEST | WIRE_SIDE_NORTH)
            else:
                self.blocks[x][2][3] = Wire(WIRE_SIDE_EAST | WIRE_SIDE_WEST)

        # Now put the input variables pins
        current_x = size_x - 1
        for input_var in term.inputs:
            self.place_pin(current_x, input_var)
            current_x -= 2

        # And same for the state variables
        for state_var in term.states:
            self.place_pin(current_x, state_var)
            current_x -= 2