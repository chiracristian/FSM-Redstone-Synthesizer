#!/bin/python3

from litemapy import Region, Schematic, BlockState
import BlockGrid

MC_DATA_VERSION: int = 4189 # Minecraft 1.21.4

def exportToLitematic(grid: BlockGrid, schematicName: str, filePath: str):
    size_x, size_y, size_z = grid.size

    region = Region(0, 0, 0, size_x, size_y, size_z)

    for x in range(size_x):
        for y in range(size_y):
            for z in range(size_z):
                block = grid.blocks[x][y][z]

                region[x, y, z] = BlockState(
                    block.name,
                    **block.getBlockStates()
                )

    schematic = region.as_schematic(schematicName, "FSM-Redstone-Synthesizer", "", MC_DATA_VERSION)

    schematic.save(filePath)
