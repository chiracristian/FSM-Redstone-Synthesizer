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

from blocks import Directions
from exporters.litematica import litematica_export
from components.upwards_wire import UpwardsWire

# Create Upwards wire
upwards_wire = UpwardsWire(100, Directions.SOUTH)

# Export to litematic
litematica_export(upwards_wire, "upwards_wire", "../output/upwards_wire.litematic")
print("Saved upwards_wire.litematic succesfully")
