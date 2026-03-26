#!/bin/python3

from blocks import Directions
from exporters.litematica import litematica_export
from components.upwards_wire import UpwardsWire

# Create Upwards wire
upwards_wire = UpwardsWire(100, Directions.SOUTH)

# Export to litematic
litematica_export(upwards_wire, "upwards_wire", "../output/upwards_wire.litematic")
print("Saved upwards_wire.litematic succesfully")
