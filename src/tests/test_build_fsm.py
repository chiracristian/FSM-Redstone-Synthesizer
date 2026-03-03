#!/bin/python3

from blocks import *
from block_grid import BlockGrid
import exporters.litematica
from fsm import *
from logic.transition_table import *
from logic.logic_minimzer import *

transition_table = TransitionTable.from_json("tests/example_machine_1101.json")
my_fsm = FSM(transition_table)

exporters.litematica.create_file(my_fsm, "my_fsm", "../output/my_fsm.litematic")
print("Saved succesfully")