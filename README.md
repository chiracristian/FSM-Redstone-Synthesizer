# FSM-Redstone-Synthesizer

A tool to automatically implement **Finite State Machines (FSM)** using Minecraft Redstone, based on given specifications in JSON files, outputting schematic files, that can be placed into your Minecraft worlds.

Instead of manually wiring the logic for complex Redstone contraptions, you can simply describe your machine's state transitions in a JSON file and this program will generate a control unit for you.

## Features
- **Logic minimization:** Highly optimized logic is generated using the Espresso algorithm (implemented in the `pyeda` library), to generate logic blocks that implement the combinational logic for calculating the output variables and what the state variables should be on the next rising edge of the clock.

- **Human-readable JSON:** The states, inputs and outputs are defined using string names. So, confusion with bit arrays is avoided.

- **Generate complete Moore machines:** This program can generate Moore FSMs (you could also try Mealy machines, but they were not tested yet). These control units are then meant to be hooked up to other components at the external input and output pins.

- **Export as ready-to-paste schematics:** The generated output files are `.litematic`, and require [Litematica mod](https://modrinth.com/mod/litematica) to be pasted in the world. As of the moment, only Litematica for Minecraft Java Edition is supported, thanks to the `litemapy` library.

- **Wide compatibility:** All the generated circuits use only long-standing intended game mechanics, the only Redstone components used being wires, torches, repeaters and comparators. So, while, at the current moment, this was tested on Minecraft Java Edition `1.21.4`, it is expected to be compatible with any Minecraft version that has the Litematica mod available. 

## Hardware architecture
The synthesizer generates a standard digital logic layout:
- **D flip-flops**: They store the machine's state and the last captured external inputs.

- **Input buses**: They carry the signals from the D flip-flops outputs to the combinational logic towers.

- **Combinational logic**: Dedicated logic towers for state transitions and external output variables.

- **Feedback lines**: Lines that take the signals from the towers that compute the next state and go to be fed back into their corresponding D flip-flops.

- **Clock bus**: A clock that goes towards all the D flip-flops, to update them, providing a stable 50/50 duty cycle.

Resulting building example:
![A top-down view of a generated Minecraft build that implements a 1101 bit sequence detector](images/1101_sequence_detector.png)

## Using with Docker on Linux
The easiest way to deploy this on Linux-based systems is using Docker
1. Clone the repository and navigate into its directory:
```bash
git clone https://github.com/chiracristian/FSM-Redstone-Synthesizer.git
cd FSM-Redstone-Synthesizer
```

2. Build the Docker image:
```bash
./build_container.sh
```

3. To use, launch the `run_container.sh` script, as in this given example:
```bash
./run_container.sh examples/simple_vending_machine.json output/vending.litematic
```

## Local installation on Linux
1. Clone the repository and navigate into its directory:
```bash
git clone https://github.com/chiracristian/FSM-Redstone-Synthesizer.git
cd FSM-Redstone-Synthesizer
```

2. Setup a python `venv`:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. To use, run the `build_fsm.py` script, like in this example
```bash
python build_fsm.py examples/1101_sequence_detector.json output/1101.litematic
```

## Example JSON for defining a FSM
Here is an example of a JSON that implements a Moore FSM that detects the `1101` sequence in the input, outputting a `1` after it is detected.

```json
{
    "info": {
        "name": "1101_sequence_detector",
        "description": "A machine that detects 1101 input sequence and outputs 1 the next clock cycle after being detected."
    },
    "config": {
        "num_inputs": 1,
        "num_state_vars": 3,
        "num_outputs": 1
    },

    "input_names": [
        {"no_input": [0]},
        {"enabled_input": [1]}
    ],
    "state_names": [
        {"initial": [0, 0, 0]},
        {"entered_1": [0, 0, 1]},
        {"entered_11": [0, 1, 0]},
        {"entered_110": [0, 1, 1]},
        {"entered_1101": [1, 0, 0]}
    ],
    "output_names": [
        {"no_output": [0]},
        {"enabled_output": [1]}
    ],

    "table": [
        { "input": "no_input", "state_t": "initial", "state_next": "initial", "output": "no_output" },
        { "input": "enabled_input", "state_t": "initial", "state_next": "entered_1", "output": "no_output" },

        { "input": "no_input", "state_t": "entered_1", "state_next": "initial", "output": "no_output" },
        { "input": "enabled_input", "state_t": "entered_1", "state_next": "entered_11", "output": "no_output" },

        { "input": "no_input", "state_t": "entered_11", "state_next": "entered_110", "output": "no_output" },
        { "input": "enabled_input", "state_t": "entered_11", "state_next": "entered_11", "output": "no_output" },

        { "input": "no_input", "state_t": "entered_110", "state_next": "initial", "output": "no_output" },
        { "input": "enabled_input", "state_t": "entered_110", "state_next": "entered_1101", "output": "no_output" },

        { "input": "no_input", "state_t": "entered_1101", "state_next": "initial", "output": "enabled_output" },
        { "input": "enabled_input", "state_t": "entered_1101", "state_next": "entered_11", "output": "enabled_output" }
    ]
}
```

## Known issues and potential improvements (feel free to contribute!)
- Up to 14 (external input variables + state variables) are currently supported, due to the generation of a layer of the towers for combinational logic not having repeaters at the long lines where the inputs are combined.
- The block-storage logic is format-agnostic. So, exporters for vanilla structure blocks or other schematic mods, maybe even some supporting other editions, like Minecraft Bedrock, could be added.
- Add the possibility to change the base blocks in a separate configuration file, without having to edit `src/blocks.py`.
- Find a more optimal layout for the feedback lines (currently they contribute the biggest delay).
- Equalize the delays of all the input buses, respectively the feedback lines, to guarantee stable Mealy machines.
