#!/bin/python3

import Blocks
from BlockGrid import BlockGrid, BlockRegion
import litematica_export

# Example: create a 3x3x3 stone cube
grid = BlockGrid(5, 5, 5)

region1 = BlockRegion(3, 3, 3)
stone = Blocks.Block(Blocks.BASE_PLATE)
for x in range(3):
    for y in range(3):
        for z in range(3):
            region1.blocks[x][y][z] = stone

region2 = BlockRegion(3, 1, 3)
my_wire = Blocks.Wire()
my_wire.east_connection = Blocks.WireConnection.SIDE
for x in range(3):
    for z in range(3):
        region2.blocks[x][0][z] = my_wire

# Paste it into grid at position (1,1,1)
grid.paste(region1, 1, 1, 1)
grid.paste(region2, 1, 4, 1)

# Export to litematic
litematica_export.exportToLitematic(grid, "stone_cube", "../output/stone_cube.litematic")
print("Saved succesfully")