#!/bin/python3

import blocks
from block_grid import BlockGrid
import exporters.litematica
import components.d_latch

# Create D latch
d_latch = components.d_latch.DLatch()

# Export to litematic
exporters.litematica.create_file(d_latch, "d_latch", "../output/d_latch.litematic")
print("Saved succesfully")