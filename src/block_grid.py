#!/bin/python3

import blocks

# X+ goes EAST
# X- goes SOUTH
# Y+ goes UP
# Y- goes DOWN
# Z+ goes SOUTH
# Z- goes NORTH

class BlockGridException(Exception):
    pass

class BlockGrid:
    def __init__(self, size_x: int, size_y: int, size_z: int):
        self.size: tuple[int, int, int] = (size_x, size_y, size_z)
        self.origin: tuple[int, int, int] = (0, 0, 0)

        # Store the blocks into a 3D array
        self.blocks = [[[blocks.Block(blocks.AIR)
                         for _ in range(size_z)]
                         for _ in range(size_y)]
                         for _ in range(size_x)]

    def paste(self, pasted_grid: "BlockGrid", 
              offset_x: int, offset_y: int, offset_z: int,
              allow_overwriting: bool = False):
        
        sx, sy, sz = pasted_grid.size
        ox, oy, oz = pasted_grid.origin

        # Iterate over blocks in pasted region space
        for x in range(sx):
            for y in range(sy):
                for z in range(sz):
                    block = pasted_grid.blocks[x][y][z]

                    # Ignore air blocks
                    if block.name == blocks.AIR:
                        continue

                    # Absolute coordinates in the grid
                    gx = offset_x + (x - ox)
                    gy = offset_y + (y - oy)
                    gz = offset_z + (z - oz)

                    # Bounds check
                    if not (0 <= gx < self.size[0] and 0 <= gy < self.size[1] and 0 <= gz < self.size[2]):
                        raise BlockGridException(f"Block at ({gx},{gy},{gz}) is out of grid bounds.")
                    
                    # Collision check
                    if (not allow_overwriting) and self.blocks[gx][gy][gz].name != "minecraft:air":
                        raise BlockGridException(f"Cannot paste block at ({gx},{gy},{gz}): space occupied.")
                    
                    # Paste the block
                    self.blocks[gx][gy][gz] = block