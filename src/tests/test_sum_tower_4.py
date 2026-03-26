#!/bin/python3

from exporters.litematica import litematica_export
from components.sum_tower import *
from logic.sop_expression import ProductTerm, LiteralState

products: list[ProductTerm] = []
products.append(ProductTerm([LiteralState.NEGATED, LiteralState.POSITIVE, LiteralState.NEGATED], 
                            [LiteralState.ABSENT, LiteralState.POSITIVE, LiteralState.NEGATED]))
products.append(ProductTerm([LiteralState.POSITIVE, LiteralState.NEGATED, LiteralState.POSITIVE], 
                            [LiteralState.POSITIVE, LiteralState.POSITIVE, LiteralState.POSITIVE]))
sum_expr = SOPExpression()
for prod in products:
    sum_expr.add_term(prod)

test_sum_tower = SumTower(sum_expr)

litematica_export(test_sum_tower, "test_sum_tower_4", "../output/test_sum_tower_4.litematic")
print("Saved test_sum_tower_4.litematic succesfully")
