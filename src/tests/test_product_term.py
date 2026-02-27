#!/bin/python3

import blocks
from block_grid import BlockGrid
import exporters.litematica
from components.product_term import ProductTermGate
from logic.sop_expression import ProductTerm, LiteralState

test_product = ProductTerm([LiteralState.POSITIVE], [LiteralState.ABSENT, LiteralState.NEGATED, LiteralState.POSITIVE])
product_term_gate = ProductTermGate(test_product)

exporters.litematica.create_file(product_term_gate, "product_term_gate", "../output/product_term_gate.litematic")
print("Saved succesfully")