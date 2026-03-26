from exporters.litematica import litematica_export
from components.clock_bus import ClockBus

clock_bus = ClockBus(20, 19)

# Export to litematic
litematica_export(clock_bus, "clock_bus", "../output/clock_bus.litematic")
print("Saved clock_bus.litematic succesfully")
