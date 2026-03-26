#!/bin/python3

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