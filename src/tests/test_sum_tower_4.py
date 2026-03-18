#!/bin/python3

from typing import List

import blocks
from block_grid import BlockGrid
import exporters.litematica
from components.sum_tower import *
from logic.sop_expression import ProductTerm, LiteralState

products: List[ProductTerm] = []
products.append(ProductTerm([LiteralState.NEGATED, LiteralState.POSITIVE, LiteralState.NEGATED], 
                            [LiteralState.ABSENT, LiteralState.POSITIVE, LiteralState.NEGATED]))
products.append(ProductTerm([LiteralState.POSITIVE, LiteralState.NEGATED, LiteralState.POSITIVE], 
                            [LiteralState.POSITIVE, LiteralState.POSITIVE, LiteralState.POSITIVE]))
sum_expr = SOPExpression()
for prod in products:
    sum_expr.add_term(prod)

test_sum_tower = SumTower(sum_expr)

exporters.litematica.litematica_export(test_sum_tower, "test_sum_tower_4", "../output/test_sum_tower_4.litematic")
print("Saved succesfully")