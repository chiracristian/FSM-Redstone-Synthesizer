#!/bin/python3

from copy import deepcopy
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

# Customizable solid blocks
BASE_PLATE = "minecraft:quartz_block"
BASE_INTERCONNECTION = "minecraft:polished_andesite"
BASE_COMBINATIONAL_BOTTOM = "minecraft:polished_diorite"
BASE_COMBINATIONAL_IN_HIGH_PIN = "minecraft:sandstone"
BASE_COMBINATIONAL_IN_LOW_PIN = "minecraft:red_sandstone"
BASE_COMBINATIONAL_OUTPUT_PIN = "minecraft:prismarie_bricks"
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

    def getBlockStates(self) -> dict[str, str]:
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

def boolToString(a: bool):
    if a:
        return "true"
    else:
        return "false"

class Wire(Block):
    def __init__(self):
        super().__init__(REDSTONE_WIRE)
        self.power: int = 0
        self.energized: bool = False
        self.north_connection: WireConnection = WireConnection.NONE
        self.south_connection: WireConnection = WireConnection.NONE
        self.east_connection: WireConnection = WireConnection.NONE
        self.west_connection: WireConnection = WireConnection.NONE

    def getBlockStates(self) -> dict[str, str]:
        result: dict = {}

        if self.energized:
            result["power"] = str(self.power)
        else:
            result["power"] = "0"

        result["north"] = self.north_connection.value
        result["south"] = self.south_connection.value
        result["east"] = self.east_connection.value
        result["west"] = self.west_connection.value

        return result

class TorchType(Enum):
    FLOOR = TORCH_FLOOR
    WALL = TORCH_WALL

class Torch(Block):
    def __init__(self, torchType: TorchType = TorchType.FLOOR, 
                 facing: Directions = Directions.INVALID):
        super.__init__(torchType.value)
        Final[self.torchType] = torchType

        self.lit: bool = True
        self.facing: Directions = facing

    def getBlockStates(self) -> dict[str, str]:
        result: dict = {}

        result["lit"] = boolToString(self.lit)
        if self.torchType is TorchType.WALL:
            result["facing"] = self.facing.value

        return result

class Repeater(Block):
    def __init__(self, facing: Directions, powered: bool = False, locked: bool = False):
        super().__init__(REPEATER)
        self.facing: Directions = facing
        self.powered: bool = powered
        self.locked: bool = locked

    def getBlockStates(self) -> dict[str, str]:
        result: dict = {}

        result["facing"] = self.facing.value
        result["powered"] = boolToString(self.powered)
        result["locked"] = boolToString(self.locked)
    
class Target(Block):
    def __init__(self):
        super().__init__(TARGET)
