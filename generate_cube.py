from litemapy import Schematic, Region, BlockState

# === CONFIG ===
MC_DATA_VERSION = 4189
SIZE = 3

air_block = BlockState("minecraft:air")
stone_block = BlockState("minecraft:stone")
dirt_block = BlockState("minecraft:dirt")
grass_block = BlockState("minecraft:grass_block")
redstone_wire = BlockState("minecraft:redstone_wire")

# Create a new schematic and a single region
region = Region(0, 0, 0, SIZE, SIZE+1, SIZE)
schem = region.as_schematic("cube_3x3x3_generated", "FSM-Redstone-Generator", "", MC_DATA_VERSION)

# Fill the region with a 3x3x3 cube of stone
for x in range(SIZE):
    for y in range(SIZE+1):
        match y:
            case 0:
                current_block = stone_block
            case 1:
                current_block = dirt_block
            case 2:
                current_block = grass_block
            case 3:
                current_block = redstone_wire
        for z in range(SIZE):
            region[x, y, z] = current_block

region[1, 3, 1] = air_block

# Save the schematic
schem.save("cube_3x3x3_generated.litematic")
print("Saved successfully!")