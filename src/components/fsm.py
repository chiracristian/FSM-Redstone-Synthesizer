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

from blocks import *
from block_grid import BlockGrid
from logic.transition_table import TransitionTable
from logic.logic_minimzer import synthesize_logic
from logic.sop_expression import SOPExpression, SOPOutput
from components.sum_tower import SumTower, SUM_TOWER_DEPTH
from components.d_flip_flop import *
from components.input_bus import *
from components.feedback_wire import *
from components.clock_bus import *

class FSM(BlockGrid):
    def __init__(self, transition_table: TransitionTable):
        # Generate the sums for next state variables and external variables output
        generated_sops: dict[SOPOutput, SOPExpression] = synthesize_logic(transition_table)
        print("Synthesized logic: ")
        print(generated_sops)

        num_inputs = transition_table.config.num_inputs
        num_state_vars = transition_table.config.num_state_vars

        # Determine the X size of the FSM
        num_tower_pins = num_inputs + num_state_vars
        num_towers = len(generated_sops.keys())

        feedback_wires_width = 2 * num_state_vars

        tower_width = 2 * num_tower_pins - 1
        between_towers_width = num_towers - 1
        towers_width = num_towers * tower_width + between_towers_width

        flip_flops_part_width = (D_FLIP_FLOP_WIDTH + 1) * num_towers

        size_x = feedback_wires_width + towers_width + flip_flops_part_width

        # Determine the Y size of the FSM
        max_tower_height = 0
        for expr in generated_sops.values():
            current_height = SumTower.determine_height(expr.terms_count())
            max_tower_height = max(max_tower_height, current_height)

        size_y = max_tower_height + 1

        # Determine the Z size of the FSM
        input_buses_z = 3 * num_towers - 1
        feedback_lines_z = 2 * num_state_vars - 1
        size_z = input_buses_z + SUM_TOWER_DEPTH + feedback_lines_z

        # Initialize the BlockGrid
        super().__init__(size_x, size_y, size_z)

        # Add a base plate
        for x in range(0, size_x):
            for z in range(0, size_z):
                self.blocks[x][0][z] = Block(BASE_PLATE)

        # Build the sum towers
        sum_towers: list[SumTower] = []
        max_tower_height = 0
        sum_towers_delay = 0
        for expr in generated_sops.values():
            current_tower = SumTower(expr)
            sum_towers.append(current_tower)

            max_tower_height = max(max_tower_height, current_tower.size[1])
            sum_towers_delay = max(sum_towers_delay, current_tower.delay)

        # Place the sum towers
        x = size_x - feedback_wires_width - tower_width
        y = 1
        z = input_buses_z
        for tower in sum_towers:
            self.paste(tower, x, y, z)
            x -= (tower_width + 1)

        def input_pin_length(i: int) -> int:
            return 3 * i + 1
        
        def input_extend_length(i: int) -> int:
            return 3 * i

        # Build the input buses
        input_buses: list[InputBus] = []
        input_buses_delay = 0
        for i in range(num_tower_pins):
            base_block = (Block(BASE_INPUT_VAR) if i < num_inputs else Block(BASE_STATE_VAR))
            
            input_bus = InputBus(base_block, num_tower_pins, i, input_pin_length(i), input_extend_length(i))
            input_buses.append(input_bus)

            input_buses_delay = max(input_buses_delay, input_bus.delay)

        # Create a d_flip_flop
        d_flip_flop = DFlipFlop()

        def input_paste_x(i: int) -> int:
            return size_x - feedback_wires_width - towers_width - 3 * i
        
        def input_paste_z(i: int) -> int:
            return input_buses_z - 1 - 3 * i

        # Create feedback lines
        feedback_lines: list[FeedbackWire] = []
        feedback_lines_delay = 0
        for i in range(num_state_vars):
            shifted_i = i + num_inputs
            extend_after_towers = 2 * i + 1
            front_wire_length = D_FLIP_FLOP_WIDTH + input_extend_length(shifted_i) + towers_width + extend_after_towers
            side_wire_length = input_pin_length(shifted_i) + SUM_TOWER_DEPTH + 2 * i

            back_wire_length = extend_after_towers
            back_wire_length += i * (tower_width + 1)
            back_wire_length += tower_width // 2 - 1

            feedback_line = FeedbackWire(front_wire_length, side_wire_length, back_wire_length, 2 * i)
            feedback_lines.append(feedback_line)

            feedback_lines_delay = max(feedback_lines_delay, feedback_line.delay)

        # Paste the input lines
        for i in range(num_tower_pins):
            in_x = input_paste_x(i)
            in_z = input_paste_z(i)

            # Paste the input lines
            self.paste(input_buses[i], in_x, 1, in_z)

            # Paste the D flip-flops
            self.paste(d_flip_flop, in_x - D_FLIP_FLOP_WIDTH, 3, in_z)

        # Paste the feedback lines
        for i in range(num_state_vars):
            in_x = input_paste_x(i+num_inputs)
            in_z = input_paste_z(i+num_inputs)
            self.paste(feedback_lines[i], in_x - D_FLIP_FLOP_WIDTH - 1, 3, in_z - 1)

        # Print delays
        print(f"Input buses delay: {input_buses_delay}")
        print(f"Combinational logic delay: {sum_towers_delay}")
        print(f"State variables feedback delay: {feedback_lines_delay}")

        total_delay = input_buses_delay + sum_towers_delay + feedback_lines_delay
        print(f"Total delay: {total_delay}")

        # Build the clock bus
        clock_bus = ClockBus(num_tower_pins, total_delay)

        # Paste the clock bus
        last_i = num_tower_pins - 1
        x = input_paste_x(last_i) - D_FLIP_FLOP_WIDTH
        y = 5
        z = input_paste_z(last_i) + D_FLIP_FLOP_DEPTH
        self.paste(clock_bus, x, y, z)

        # Propagate all the lit torches from the towers
        self.propagate_all_torches()
