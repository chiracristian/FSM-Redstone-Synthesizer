#!/bin/python3

from litemapy import Region, BlockState
import block_grid

MC_DATA_VERSION: int = 4189 # Minecraft 1.21.4

def create_file(grid: block_grid, schematic_name: str, output_file_path: str):
    size_x, size_y, size_z = grid.size

    region = Region(0, 0, 0, size_x, size_y, size_z)

    for x in range(size_x):
        for y in range(size_y):
            for z in range(size_z):
                block = grid.blocks[x][y][z]

                region[x, y, z] = BlockState(
                    block.name,
                    **block.get_block_states()
                )

    schematic = region.as_schematic(schematic_name, "FSM-Redstone-Synthesizer", "", MC_DATA_VERSION)

    schematic.save(output_file_path)
