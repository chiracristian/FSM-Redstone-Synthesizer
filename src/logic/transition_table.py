import json
from typing import List, Dict, Any

class TransitionTable:
    def __init__(self, num_inputs: int, num_states: int, num_outputs: int):
        self.num_inputs = num_inputs
        self.num_state_vars = num_states
        self.num_outputs = num_outputs
        
        # The table is a list of dictionaries representing each row
        self.rows: List[Dict[str, List[int]]] = []

    @classmethod
    def from_json(cls, file_path: str) -> 'TransitionTable':
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Metadata configuration
        config = data.get("config", {})
        n_in = config.get("num_inputs", 1)
        n_st = config.get("num_state_vars", 1)
        n_out = config.get("num_outputs", 1)
        
        table = cls(n_in, n_st, n_out)
        
        # Load rows
        # Expected JSON format: list of objects with "input", "state_t", "state_next", "output"
        for entry in data.get("table", []):
            row = {
                "input": entry["input"],           # e.g., [0, 1]
                "state_t": entry["state_t"],       # e.g., [0, 0, 1]
                "state_next": entry["state_next"], # e.g., [0, 1, 0]
                "output": entry["output"]          # e.g., [1, 0]
            }
            
            # Check if row dimension matches
            if len(row["input"]) != n_in or len(row["state_t"]) != n_st:
                raise ValueError(f"Row dimension mismatch in {file_path}")
                
            table.rows.append(row)
            
        return table

    def get_next_state(self, current_state: List[int], inputs: List[int]) -> List[int]:
        """Lookup delta(s, i)"""
        for row in self.rows:
            if row["state_t"] == current_state and row["input"] == inputs:
                return row["state_next"]
            
        raise ValueError(f"Failed to find row with inputs {inputs} and current state {current_state}")