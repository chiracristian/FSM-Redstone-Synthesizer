#!/bin/python3

from blocks import *
from block_grid import BlockGrid
import exporters.litematica
import components.downwards_wire

# Create Upwards wire
downwards_wire = components.downwards_wire.DownwardsOrWire(16)

# Export to litematic
exporters.litematica.litematica_export(downwards_wire, "downwards_wire", "../output/downwards_wire.litematic")
print("Saved succesfully")