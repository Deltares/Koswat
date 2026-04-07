#!/bin/sh
set -e

echo "Running pixi lock before version bump..."
pixi lock

echo "Staging pixi.lock..."
git add pixi.lock

echo "pixi lock completed successfully."