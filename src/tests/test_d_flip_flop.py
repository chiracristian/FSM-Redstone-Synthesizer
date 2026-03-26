#!/bin/python3

from exporters.litematica import litematica_export
from components.d_flip_flop import DFlipFlop

# Create D flip flop
d_flip_flop = DFlipFlop()

# Export to litematic
litematica_export(d_flip_flop, "d_flip_flop", "../output/d_flip_flop.litematic")
print("Saved d_flip_flop.litematic succesfully")
