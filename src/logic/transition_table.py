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

from dataclasses import dataclass
import json
from components.product_term import PRODUCT_TERM_MAX_INPUTS

@dataclass
class TransitionTableInfo:
    name: str
    description: str

@dataclass
class TransitionTableConfig:
    num_inputs: int
    num_state_vars: int
    num_outputs: int

class TransitionTable:
    """Represents a transition table for a FSM"""
    def __init__(self, info: TransitionTableInfo, config: TransitionTableConfig):
        self.info = info
        self.config = config
        
        # The table remains a list of dictionaries representing each row with bit-arrays
        self.rows: list[dict[str, list[int]]] = []

    @classmethod
    def from_json(cls, file_path: str) -> 'TransitionTable':
        """Loads a transition table from a JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Parse info
        info_data = data.get("info", {})
        info = TransitionTableInfo(
            name=info_data.get("name", "unnamed_machine"),
            description=info_data.get("description", "")
        )

        # Parse configuration
        conf_data = data.get("config", {})
        config = TransitionTableConfig(
            num_inputs=conf_data.get("num_inputs", 1),
            num_state_vars=conf_data.get("num_state_vars", 1),
            num_outputs=conf_data.get("num_outputs", 1)
        )

        # Ensure we have at least one input, one state variable and one output
        if config.num_inputs < 1 or config.num_state_vars < 1 or config.num_outputs < 1:
            raise ValueError("There must be at least one input, one state variable and one output")
        
        # Check the number of (inputs + state variables)
        if (config.num_inputs + config.num_state_vars) > PRODUCT_TERM_MAX_INPUTS:
            raise ValueError(f"The total number of external inputs and state variables can be at most {PRODUCT_TERM_MAX_INPUTS}")

        # Create lookup dictionaries from the name mapping lists
        input_map = cls._parse_name_map(data.get("input_names", []))
        state_map = cls._parse_name_map(data.get("state_names", []))
        output_map = cls._parse_name_map(data.get("output_names", []))
        
        table = cls(info, config)
        
        # Load and resolve names into bit-arrays
        for entry in data.get("table", []):
            try:
                row = {
                    "input": input_map[entry["input"]],
                    "state_t": state_map[entry["state_t"]],
                    "state_next": state_map[entry["state_next"]],
                    "output": output_map[entry["output"]]
                }
            except KeyError as e:
                raise KeyError(f"Label {e} not found in the mapping definitions of {file_path}")
            
            # Validation: Ensure the resolved bit-arrays match the config
            cls._validate_row(row, config, file_path)
            table.rows.append(row)
            
        return table

    @staticmethod
    def _parse_name_map(mapping_list: list[dict]) -> dict[str, list[int]]:
        """Flattens the JSON name mapping list into a single lookup dictionary."""
        lookup = {}
        for entry in mapping_list:
            for name, bits in entry.items():
                lookup[name] = bits
        return lookup

    @staticmethod
    def _validate_row(row, config, file_path):
        """Internal helper to ensure JSON data matches the defined bit-widths."""
        if len(row["input"]) != config.num_inputs:
            raise ValueError(f"Input dimension mismatch in {file_path}: expected {config.num_inputs}")
        if len(row["state_t"]) != config.num_state_vars:
            raise ValueError(f"State dimension mismatch in {file_path}: expected {config.num_state_vars}")
        if len(row["output"]) != config.num_outputs:
            raise ValueError(f"Output dimension mismatch in {file_path}: expected {config.num_outputs}")

    def get_next_state(self, current_state: list[int], inputs: list[int]) -> list[int]:
        """Lookup the next state for a given current state and inputs."""
        for row in self.rows:
            if row["state_t"] == current_state and row["input"] == inputs:
                return row["state_next"]
            
        raise ValueError(f"Failed to find row with inputs {inputs} and current state {current_state}")
