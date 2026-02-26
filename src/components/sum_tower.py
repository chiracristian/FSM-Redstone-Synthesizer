#!/bin/python3

from typing import List

from blocks import *
from block_grid import BlockGrid
from logic.sop_expression import *
from components.product_term import *
from components.upwards_wire import *
from components.downwards_wire import *

class SumTower(BlockGrid):
    def __init__(self, expression: SOPExpression):

        product_term_gates: List[ProductTermGate] = []
        for term in expression.terms:
            product_term_gates.append(ProductTermGate(term))

        gate_width = product_term_gates[0].size[0]
        gate_count = len(product_term_gates)
        variables_count = product_term_gates[0].input_pins_count

        # 4 is the minimal width, in case we have only one state variable and input
        size_x = max(4, gate_width)
        size_y = PRODUCT_TERM_HEIGHT * gate_count + 3
        size_z = EFFECTIVE_UPWARDS_WIRE_DEPTH + PRODUCT_TERM_DEPTH + DOWNWARDS_OR_WIRE_DEPTH

        super().__init__(size_x, size_y, size_z)

        # Paste the product term gates
        current_y = 1
        for gate in product_term_gates:
            self.paste(gate, 0, current_y, EFFECTIVE_UPWARDS_WIRE_DEPTH)
            current_y += PRODUCT_TERM_HEIGHT

        # Create the upward input wires
        input_wire = UpwardsWire(current_y - 2, Directions.NORTH)

        # Place the input wires (with repeaters in front)
        for x in range(0, 2 * variables_count, 2):
            self.blocks[x][0][1] = Block(BASE_COMBINATIONAL_BOTTOM)
            self.blocks[x][1][1] = Repeater(Directions.NORTH)
            self.paste(input_wire, x, 0, 0)

        # Build and place the downwards wire
        downwards_wire = DownwardsOrWire(gate_count)
        torches_x = product_term_gates[0].out_torch_x
        self.paste(downwards_wire, torches_x - 2, 1, EFFECTIVE_UPWARDS_WIRE_DEPTH + PRODUCT_TERM_DEPTH)
