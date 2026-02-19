#!/bin/python3

from enum import Enum
from tokenize import String
from typing import Final

# -----------------------------------------------------------------------------
# BLOCK IDs LIST
# -----------------------------------------------------------------------------

# May NOT be customized
AIR = "minecraft:air"
REDSTONE_WIRE = "minecraft:redstone_wire"
REPEATER = "minecraft:repeater"
COMPARATOR = "minecraft:comparator"
TORCH_FLOOR = "minecraft:redstone_torch"
TORCH_WALL = "minecraft:redstone_wall_torch"
TARGET = "minecraft:target"
COPPER_BULB = "minecraft:waxed_copper_bulb"
DROPPER = "minecraft:dropper"

# Customizable solid blocks
BASE_PLATE = "minecraft:quartz_block"
BASE_INTERCONNECTION = "minecraft:polished_andesite"
BASE_COMBINATIONAL_BOTTOM = "minecraft:polished_diorite"
BASE_COMBINATIONAL_IN_HIGH_PIN = "minecraft:sandstone"
BASE_COMBINATIONAL_IN_LOW_PIN = "minecraft:red_sandstone"
BASE_COMBINATIONAL_OUTPUT_PIN = "minecraft:prismarie_bricks"
BASE_SEQUENTIAL = "minecraft:lime_concrete"
BASE_SEQUENTIAL_D_PIN = "minecraft:lime_concrete"
BASE_SEQUENTIAL_CLK_PIN = "minecraft:magenta_concrete"
BASE_SEQUENTIAL_Q_PIN = "minecraft:orange_concrete"

# Customizable transparent blocks
BASE_UPWARDS_COMBINATIONAL_WIRING = "minecraft:white_stained_glass"

# -----------------------------------------------------------------------------
# Definition of block classes
# -----------------------------------------------------------------------------
class Block:
    def __init__(self, name: str):
        self.name: str = name

    def get_block_states(self) -> dict[str, str]:
        return {}

class Directions(Enum):
    INVALID = None
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"

class WireConnection(Enum):
    NONE = "none"
    SIDE = "side"
    UP = "up"

def bool_to_string(a: bool):
    if a:
        return "true"
    else:
        return "false"
    
WIRE_SIDE_NORTH = 1 << 0
WIRE_SIDE_SOUTH = 1 << 1
WIRE_SIDE_EAST = 1 << 2
WIRE_SIDE_WEST = 1 << 3
WIRE_UP_NORTH = 1 << 4
WIRE_UP_SOUTH = 1 << 5
WIRE_UP_EAST = 1 << 6
WIRE_UP_WEST = 1 << 7
MAX_WIRE_POWER = 15

class Wire(Block):
    def set_sides(self, sides: int):
        # North
        if sides & WIRE_SIDE_NORTH:
            self.north_connection = WireConnection.SIDE
        elif sides & WIRE_UP_NORTH:
            self.north_connection = WireConnection.UP
        else:
            self.north_connection = WireConnection.NONE

        # South
        if sides & WIRE_SIDE_SOUTH:
            self.south_connection = WireConnection.SIDE
        elif sides & WIRE_UP_SOUTH:
            self.south_connection = WireConnection.UP
        else:
            self.south_connection = WireConnection.NONE

        # East
        if sides & WIRE_SIDE_EAST:
            self.east_connection = WireConnection.SIDE
        elif sides & WIRE_UP_EAST:
            self.east_connection = WireConnection.UP
        else:
            self.east_connection = WireConnection.NONE

        # West
        if sides & WIRE_SIDE_WEST:
            self.west_connection = WireConnection.SIDE
        elif sides & WIRE_UP_WEST:
            self.west_connection = WireConnection.UP
        else:
            self.west_connection = WireConnection.NONE

    def __init__(self, sides: int = 0):
        super().__init__(REDSTONE_WIRE)
        self.power: int = 0

        self.north_connection: WireConnection = WireConnection.NONE
        self.south_connection: WireConnection = WireConnection.NONE
        self.east_connection: WireConnection = WireConnection.NONE
        self.west_connection: WireConnection = WireConnection.NONE
        self.set_sides(sides)

    def is_energized(self) -> bool:
        return self.power > 0

    def get_block_states(self) -> dict[str, str]:
        result: dict = {}

        result["power"] = str(self.power)

        result["north"] = self.north_connection.value
        result["south"] = self.south_connection.value
        result["east"] = self.east_connection.value
        result["west"] = self.west_connection.value

        return result

class TorchType(Enum):
    FLOOR = TORCH_FLOOR
    WALL = TORCH_WALL

class Torch(Block):
    def __init__(self, torch_type: TorchType = TorchType.FLOOR, 
                 facing: Directions = Directions.INVALID):
        super().__init__(torch_type.value)
        self.torch_type = torch_type

        self.lit: bool = True
        self.facing: Directions = facing

    def get_block_states(self) -> dict[str, str]:
        result: dict = {}

        result["lit"] = bool_to_string(self.lit)
        if self.torch_type is TorchType.WALL:
            result["facing"] = self.facing.value

        return result

class Repeater(Block):
    def __init__(self, facing: Directions, powered: bool = False, locked: bool = False):
        super().__init__(REPEATER)
        self.facing: Directions = facing
        self.powered: bool = powered
        self.locked: bool = locked

    def get_block_states(self) -> dict[str, str]:
        result: dict = {}

        result["facing"] = self.facing.value
        result["powered"] = bool_to_string(self.powered)
        result["locked"] = bool_to_string(self.locked)

        return result

class Comparator(Block):
    def __init__(self, facing: Directions):
        super().__init__(COMPARATOR)
        self.facing: Directions = facing

    def get_block_states(self) -> dict[str, str]:
        result: dict = {}

        result["facing"] = self.facing.value

        return result
    
class Dropper(Block):
    def __init__(self, facing: Directions, triggered: bool = False):
        super().__init__(DROPPER)
        self.facing: Directions = facing
        self.triggered: bool = triggered

    def get_block_states(self) -> dict[str, str]:
        result: dict = {}

        result["facing"] = self.facing.value
        result["triggered"] = bool_to_string(self.triggered)

        return result
