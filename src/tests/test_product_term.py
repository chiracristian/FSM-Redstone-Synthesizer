#!/bin/python3

from exporters.litematica import litematica_export
from components.product_term import ProductTermGate
from logic.sop_expression import ProductTerm, LiteralState

test_product = ProductTerm([LiteralState.POSITIVE], [LiteralState.ABSENT, LiteralState.NEGATED, LiteralState.POSITIVE])
product_term_gate = ProductTermGate(test_product)

litematica_export(product_term_gate, "product_term_gate", "../output/product_term_gate.litematic")
print("Saved product_term_gate.litematic succesfully")
