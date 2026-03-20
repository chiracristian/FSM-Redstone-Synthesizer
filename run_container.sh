#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: ./run_container.sh <input_json> <output_litematic>"
    echo "Example: ./run_container.sh examples/1101_sequence_detector.json output/1101_detector.litematic"
    exit 1
fi

INPUT_FILE=$1
OUTPUT_FILE=$2
IMAGE_NAME="fsm-redstone-synthesizer:latest"

# Run the container with the current user
docker run --rm \
  -u "$(id -u):$(id -g)" \
  -v "$(pwd)":/app \
  "$IMAGE_NAME" \
  "$INPUT_FILE" \
  "$OUTPUT_FILE"
