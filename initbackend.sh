#!/usr/bin/env bash

set -e

ROOT="project-root"

echo "📁 Creating directories (if not exist)..."

mkdir -p \
  $ROOT/cmd/api \
  $ROOT/internal/handlers \
  $ROOT/internal/services \
  $ROOT/internal/repositories \
  $ROOT/internal/models \
  $ROOT/internal/auth \
  $ROOT/internal/config \
  $ROOT/internal/utils \
  $ROOT/pkg \
  $ROOT/migrations

echo "📄 Creating files (if not exist)..."

touch \
  $ROOT/go.mod \
  $ROOT/go.sum \
  \
  $ROOT/cmd/api/main.go \
  \
  $ROOT/internal/handlers/auth_handler.go \
  $ROOT/internal/handlers/doctor_handler.go \
  $ROOT/internal/handlers/appointment_handler.go \
  $ROOT/internal/handlers/admin_handler.go \
  $ROOT/internal/handlers/payment_handler.go \
  \
  $ROOT/internal/services/auth_service.go \
  $ROOT/internal/services/doctor_service.go \
  $ROOT/internal/services/appointment_service.go \
  $ROOT/internal/services/payment_service.go \
  $ROOT/internal/services/notification_service.go \
  \
  $ROOT/internal/repositories/user_repo.go \
  $ROOT/internal/repositories/doctor_repo.go \
  $ROOT/internal/repositories/appointment_repo.go \
  $ROOT/internal/repositories/transaction_repo.go \
  \
  $ROOT/internal/models/user.go \
  $ROOT/internal/models/doctor.go \
  $ROOT/internal/models/appointment.go \
  $ROOT/internal/models/transaction.go \
  $ROOT/internal/models/wallet.go \
  \
  $ROOT/internal/auth/jwt.go \
  $ROOT/internal/auth/middleware.go \
  \
  $ROOT/internal/config/config.go \
  \
  $ROOT/internal/utils/validator.go \
  $ROOT/internal/utils/response.go \
  $ROOT/internal/utils/errors.go \
  \
  $ROOT/.env \
  $ROOT/Dockerfile \
  $ROOT/docker-compose.yml

echo "✍️ Writing main.go (only if empty)..."

MAIN_FILE="$ROOT/cmd/api/main.go"

if [ ! -s "$MAIN_FILE" ]; then
cat << 'EOF' > "$MAIN_FILE"
package main

import (
	"log"

	"yourproject/internal/config"
	"yourproject/internal/server"
)

func main() {
	cfg := config.Load()
	app := server.New(cfg)
	log.Fatal(app.Run(cfg.Port))
}
EOF
else
  echo "⚠️ main.go already has content — skipped overwrite"
fi

echo "✅ Project structure initialized successfully (non-destructive)."
