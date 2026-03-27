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

from litemapy import Region, BlockState
from block_grid import BlockGrid

MC_DATA_VERSION: int = 4189 # Minecraft 1.21.4

def litematica_export(grid: BlockGrid, schematic_name: str, output_file_path: str):
    """Exports a BlockGrid as a Litematica schematic file."""
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
