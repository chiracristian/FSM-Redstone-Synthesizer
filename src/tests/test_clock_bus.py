import blocks
from block_grid import BlockGrid
import exporters.litematica
from components.clock_bus import ClockBus

clock_bus = ClockBus(20, 19)

# Export to litematic
exporters.litematica.litematica_export(clock_bus, "clock_bus", "../output/clock_bus.litematic")
print("Saved succesfully")