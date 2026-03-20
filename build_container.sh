#!/bin/bash

# Exit on any error
set -e

IMAGE_NAME="fsm-redstone-synthesizer"
TAG="latest"

echo "[*] Building Docker image: $IMAGE_NAME:$TAG..."
docker build -t "$IMAGE_NAME:$TAG" .

echo "[+] Build complete!"
