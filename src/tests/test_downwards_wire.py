#!/bin/python3

from exporters.litematica import litematica_export
from components.downwards_wire import DownwardsOrWire

# Create Upwards wire
downwards_wire = DownwardsOrWire(16)

# Export to litematic
litematica_export(downwards_wire, "downwards_wire", "../output/downwards_wire.litematic")
print("Saved downwards_wire.litematic succesfully")
