#!/bin/python3

import blocks
from block_grid import BlockGrid
import exporters.litematica
import components.d_flip_flop

# Create D flip flop
d_flip_flop = components.d_flip_flop.DFlipFlop()

# Export to litematic
exporters.litematica.create_file(d_flip_flop, "d_flip_flop", "../output/d_flip_flop.litematic")
print("Saved succesfully")