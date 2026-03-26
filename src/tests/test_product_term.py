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

from exporters.litematica import litematica_export
from components.product_term import ProductTermGate
from logic.sop_expression import ProductTerm, LiteralState

test_product = ProductTerm([LiteralState.POSITIVE], [LiteralState.ABSENT, LiteralState.NEGATED, LiteralState.POSITIVE])
product_term_gate = ProductTermGate(test_product)

litematica_export(product_term_gate, "product_term_gate", "../output/product_term_gate.litematic")
print("Saved product_term_gate.litematic succesfully")
