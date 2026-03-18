#!/bin/python3

from blocks import *
from block_grid import BlockGrid
import exporters.litematica
import components.upwards_wire

# Create Upwards wire
upwards_wire = components.upwards_wire.UpwardsWire(100, Directions.SOUTH)

# Export to litematic
exporters.litematica.litematica_export(upwards_wire, "upwards_wire", "../output/upwards_wire.litematic")
print("Saved succesfully")