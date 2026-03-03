from blocks import *
from block_grid import BlockGrid
from logic.transition_table import TransitionTable
from logic.logic_minimzer import synthesize_logic
from logic.sop_expression import SOPExpression, SOPOutput
from components.sum_tower import SumTower

TOWERS_SPACING = 2

class FSM(BlockGrid):
    def __init__(self, transition_table: TransitionTable):
        generated_sops: dict[SOPOutput, SOPExpression] = synthesize_logic(transition_table)
        print(generated_sops)

        sum_towers: list[SumTower] = []
        towers_x_span = 0
        towers_y_span = 0
        towers_z_span = 0
        for sop in generated_sops.values():
            current_tower = SumTower(sop)
            sum_towers.append(current_tower)
            towers_x_span += current_tower.size[0]
            towers_y_span = max(towers_y_span, current_tower.size[1])
            towers_z_span = max(towers_z_span, current_tower.size[2])

        if len(sum_towers) > 1:
            towers_x_span += TOWERS_SPACING * (len(sum_towers) - 1)

        size_x = towers_x_span
        size_y = towers_y_span
        size_z = towers_z_span
        super().__init__(size_x, size_y, size_z)

        # Paste towers from right to left (standard for bus layout)
        current_x = towers_x_span
        for tower in sum_towers:
            # We want to paste at the start of the tower's X-range
            current_x -= tower.size[0]
            self.paste(tower, current_x, 0, 0)
            current_x -= TOWERS_SPACING
