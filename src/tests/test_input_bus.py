#!/bin/python3

from blocks import *
from block_grid import BlockGrid
import exporters.litematica
from fsm import *
from logic.transition_table import *
from logic.logic_minimzer import *
from components.input_bus import *

transition_table = TransitionTable.from_json("tests/example_machine_drinks.json")

generated_sops: dict[SOPOutput, SOPExpression] = synthesize_logic(transition_table)
print(generated_sops)

sum_towers: list[SumTower] = []
towers_x_span = 0
towers_y_span = 0
towers_z_span = 0
pins_per_tower = transition_table.num_inputs + transition_table.num_state_vars

for sop in generated_sops.values():
    current_tower = SumTower(sop)
    sum_towers.append(current_tower)
    towers_x_span += current_tower.size[0]
    towers_y_span = max(towers_y_span, current_tower.size[1])
    towers_z_span = max(towers_z_span, current_tower.size[2])

tower_width = sum_towers[0].size[0]
towers_count = len(sum_towers)
if towers_count > 1:
    towers_x_span += TOWERS_SPACING * (towers_count - 1)

input_bus = InputBus(Block(BASE_STATE_VAR), towers_count, tower_width, 3, 9, 6)

exporters.litematica.create_file(input_bus, "input_bus", "../output/input_bus.litematic")
print("Saved succesfully")