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

import blocks
from block_grid import BlockGrid
import exporters.litematica

# Example: create a 3x3x3 stone cube
grid = BlockGrid(5, 5, 5)

region1 = BlockGrid(3, 3, 3)
my_stone = blocks.Block(blocks.BASE_COMBINATIONAL_BOTTOM)
for x in range(3):
    for y in range(3):
        for z in range(3):
            region1.blocks[x][y][z] = my_stone

region2 = BlockGrid(3, 1, 3)
my_wire = blocks.Wire()
my_wire.east_connection = blocks.WireConnection.SIDE
for x in range(3):
    for z in range(3):
        region2.blocks[x][0][z] = my_wire

# Paste it into grid at position (1,1,1)
grid.paste(region1, 1, 1, 1)
grid.paste(region2, 1, 4, 1)

# Export to litematic
exporters.litematica.litematica_export(grid, "stone_cube", "../output/stone_cube.litematic")
print("Saved succesfully")