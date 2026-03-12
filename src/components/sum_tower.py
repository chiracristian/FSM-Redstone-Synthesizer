#!/bin/python3

from blocks import *
from block_grid import BlockGrid
from logic.sop_expression import *
from components.product_term import *
from components.upwards_wire import *
from components.downwards_wire import *

TOWERS_SPACING = 1
SUM_TOWER_DEPTH = EFFECTIVE_UPWARDS_WIRE_DEPTH + PRODUCT_TERM_DEPTH + DOWNWARDS_OR_WIRE_DEPTH

class SumTower(BlockGrid):
    def __init__(self, expression: SOPExpression):
        product_term_gates: list[ProductTermGate] = []
        for term in expression.terms:
            product_term_gates.append(ProductTermGate(term))

        gate_width = product_term_gates[0].size[0]
        gate_count = len(product_term_gates)
        input_vars_count = product_term_gates[0].inputs_count
        state_vars_count = product_term_gates[0].state_vars_count

        # 4 is the minimal width, in case we have only one state variable and input
        size_x = max(4, gate_width)
        size_y = PRODUCT_TERM_HEIGHT * gate_count + 3
        size_z = SUM_TOWER_DEPTH

        super().__init__(size_x, size_y, size_z)

        # Paste the product term gates
        current_y = 1
        for gate in product_term_gates:
            self.paste(gate, 0, current_y, EFFECTIVE_UPWARDS_WIRE_DEPTH)
            current_y += PRODUCT_TERM_HEIGHT

        # Create the upward wires
        input_var_wire = UpwardsWire(current_y - 2, Directions.NORTH, Block(BASE_UPWARDS_INPUT_VAR))
        state_var_wire = UpwardsWire(current_y - 2, Directions.NORTH, Block(BASE_UPWARDS_STATE_VAR))

        # Place the vertical wires (with repeaters in front)
        x = 0

        for _ in range(0, state_vars_count):
            self.blocks[x][0][1] = Block(BASE_STATE_VAR)
            self.blocks[x][1][1] = Repeater(Directions.NORTH)
            self.paste(state_var_wire, x, 0, 0)
            x += 2

        for _ in range(0, input_vars_count):
            self.blocks[x][0][1] = Block(BASE_INPUT_VAR)
            self.blocks[x][1][1] = Repeater(Directions.NORTH)
            self.paste(input_var_wire, x, 0, 0)
            x += 2

        # Build and place the downwards wire
        downwards_wire = DownwardsOrWire(gate_count)
        torches_x = product_term_gates[0].out_torch_x
        self.paste(downwards_wire, torches_x - 2, 1, EFFECTIVE_UPWARDS_WIRE_DEPTH + PRODUCT_TERM_DEPTH)

        # Calculate the total delay due to
        # - repeaters before vertical wires (1)
        # - the vertical wires
        # - the output ORing wire
        self.delay = 1 + state_var_wire.delay + product_term_gates[0].delay + downwards_wire.delay
