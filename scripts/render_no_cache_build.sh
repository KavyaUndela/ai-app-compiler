#!/usr/bin/env bash
set -euo pipefail

# Local helper: build the project Docker image without using any cache.
# Usage: ./scripts/render_no_cache_build.sh [image:tag]
# Example: ./scripts/render_no_cache_build.sh ai-app-compiler:latest

IMAGE_TAG=${1:-ai-app-compiler:local}

echo "Building Docker image (no cache): $IMAGE_TAG"
DOCKER_BUILDKIT=1 docker build --no-cache -t "$IMAGE_TAG" -f Dockerfile .

echo "Build complete: $IMAGE_TAG"

echo "If you need to push this image to a registry, run:"
echo "  docker tag $IMAGE_TAG <registry>/<repo>:$IMAGE_TAG && docker push <registry>/<repo>:$IMAGE_TAG"
