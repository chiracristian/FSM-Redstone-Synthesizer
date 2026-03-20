#!/usr/bin/env python3
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