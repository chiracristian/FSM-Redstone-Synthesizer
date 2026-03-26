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

import sys
import argparse
from pathlib import Path

# Ensure the src directory is in the path so imports work
sys.path.append(str(Path(__file__).parent / "src"))

from src.logic.transition_table import TransitionTable
from src.components.fsm import FSM
from src.exporters.litematica import litematica_export

def main():
    parser = argparse.ArgumentParser(description="Minecraft Redstone FSM Synthesizer")
    parser.add_argument("input", help="Path to the input transition table JSON")
    parser.add_argument("output", help="Path to save the generated .litematic file")
    
    args = parser.parse_args()

    # Validate File Extensions
    input_path = Path(args.input)
    output_path = Path(args.output)

    if input_path.suffix.lower() != ".json":
        print(f"[-] Error: Input file must be a .json file (got {input_path.suffix})")
        sys.exit(1)

    if output_path.suffix.lower() != ".litematic":
        print(f"[-] Error: Output file must have a .litematic extension (got {output_path.suffix})")
        sys.exit(1)

    # Load the transition table file
    print(f"[*] Loading transition table from {args.input} ...\n")
    
    table = TransitionTable.from_json(args.input)

    # Output name and description
    print(f"[*] Loaded {table.info.name}")
    print(f"[*] Description: {table.info.description}\n")

    # Synthesize logic and build the structure
    print(f"[*] Synthesizing logic and building FSM structure")
    fsm_grid = FSM(table)

    # Export to Litematica
    print(f"\n[*] Exporting to {args.output} ...")
    litematica_export(fsm_grid, table.info.name, args.output)

    print("[+] Success!")

if __name__ == "__main__":
    main()