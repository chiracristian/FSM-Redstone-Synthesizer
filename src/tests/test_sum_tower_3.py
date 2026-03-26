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
from components.sum_tower import *
from logic.sop_expression import ProductTerm, LiteralState

products: list[ProductTerm] = []
products.append(ProductTerm([LiteralState.NEGATED], [LiteralState.ABSENT, LiteralState.POSITIVE, LiteralState.NEGATED]))
products.append(ProductTerm([LiteralState.POSITIVE], [LiteralState.POSITIVE, LiteralState.POSITIVE, LiteralState.POSITIVE]))
sum_expr = SOPExpression()
for prod in products:
    sum_expr.add_term(prod)

test_sum_tower = SumTower(sum_expr)

litematica_export(test_sum_tower, "test_sum_tower_3", "../output/test_sum_tower_3.litematic")
print("Saved test_sum_tower_3.litematic succesfully")
