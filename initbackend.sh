#!/usr/bin/env bash

set -e

ROOT="project-root"

# --------------------
# Directories
# --------------------
mkdir -p \
  $ROOT/cmd/api \
  $ROOT/internal/handlers \
  $ROOT/internal/services \
  $ROOT/internal/repositories \
  $ROOT/internal/models \
  $ROOT/internal/auth \
  $ROOT/internal/config \
  $ROOT/internal/utils \
  $ROOT/pkg

# --------------------
# Files
# --------------------
touch \
  $ROOT/cmd/api/main.go \
  \
  $ROOT/go.mod \
  $ROOT/go.sum

echo "✅ Project structure created successfully."
