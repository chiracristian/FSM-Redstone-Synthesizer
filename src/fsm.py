from blocks import *
from block_grid import BlockGrid
from logic.transition_table import TransitionTable
from logic.logic_minimzer import synthesize_logic
from logic.sop_expression import SOPExpression, SOPOutput, SOPOutputType
from components.sum_tower import SumTower, TOWERS_SPACING
from components.d_flip_flop import *
from components.input_bus import *
from components.feedback_wire import *

class FSM(BlockGrid):
    def __init__(self, transition_table: TransitionTable):
        generated_sops: dict[SOPOutput, SOPExpression] = synthesize_logic(transition_table)
        print(generated_sops)

        # Construct the towers
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

        def is_external_var_in(pin_idx: int) -> bool:
            return pin_idx < transition_table.num_inputs

        # Construct the input buses
        input_buses: list[InputBus] = []
        input_buses_x: list[int] = []
        current_pin_len = -2
        extend_to_flip_flop_len = -D_FLIP_FLOP_WIDTH - 1
        
        for pin_idx in range(0, pins_per_tower):
            base_block = (Block(BASE_INPUT_VAR) if is_external_var_in(pin_idx) else Block(BASE_STATE_VAR))

            current_pin_len += 3
            extend_to_flip_flop_len += 3

            input_bus = InputBus(base_block, towers_count, tower_width, 
                                  pin_idx, current_pin_len, extend_to_flip_flop_len)
            input_buses.append(input_bus)
            input_buses_x.append(extend_to_flip_flop_len)

        input_buses_span: tuple[int, int, int] = (0, 0, 0)
        max_bus_width = 0
        for bus in input_buses:
            if bus.size[0] >= max_bus_width:
                max_bus_width = bus.size[0]
                input_buses_span = bus.size

        output_pins_extent = (transition_table.num_state_vars - 1) * 2 + 1

        size_x = max(towers_x_span + 1, input_buses_span[0] + input_buses_x[-1] + D_FLIP_FLOP_WIDTH + 1)
        size_y = max(towers_y_span, input_buses_span[1])
        size_z = towers_z_span + input_buses_span[2] + output_pins_extent
        super().__init__(size_x, size_y, size_z)

        # Add a base plate
        for x in range(0, size_x):
            for z in range(0, size_z):
                self.blocks[x][0][z] = Block(BASE_PLATE)

        # Paste towers (left to right)
        TOWERS_X_OFFSET = 2 * transition_table.num_state_vars
        current_x = size_x - TOWERS_X_OFFSET
        towers_z = input_buses_span[2]
        towers_delay = 0
        for tower in sum_towers:
            current_x -= tower_width
            self.paste(tower, current_x, 1, towers_z)
            current_x -= TOWERS_SPACING
            towers_delay = max(towers_delay, tower.delay)

        # Paste inputs, D latches or flip flops and feedback lines
        last_in_i = 0
        input_bus_delay = 0
        feedback_wire_delay = 0
        for i, (bus, bus_x) in enumerate(zip(input_buses, input_buses_x)):
            x = size_x - towers_x_span - bus_x - TOWERS_X_OFFSET
            z = towers_z - bus.size[2] + 1
            self.paste(bus, x, 1, z)
            input_bus_delay = max(input_bus_delay, bus.delay)

            y = INPUT_BUS_HEIGHT - 1

            # Put a D flip flop in front of the input line
            self.paste(DFlipFlop(), x - D_FLIP_FLOP_WIDTH, y, z)
            
            if is_external_var_in(i):
                last_in_i = i
            else:
                # Put the feedback line
                tower_idx = i - (last_in_i + 1)
                feedback_wire = FeedbackWire(towers_x_span, tower_width, tower_idx, bus_x, bus.size[2])
                feedback_wire_delay = max(feedback_wire_delay, feedback_wire.delay)
                self.paste(feedback_wire, x - D_FLIP_FLOP_WIDTH - 1, y, z - 1, True)

        print(f"Input bus delay: {input_bus_delay}")
        print(f"Towers delay: {towers_delay}")
        print(f"Output feedback delay: {feedback_wire_delay}")
        total_delay = input_bus_delay + towers_delay + feedback_wire_delay
        print(f"Total delay: {total_delay}")
