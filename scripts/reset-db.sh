#!/bin/bash
# Reset database volumes and recreate from scratch
# This script stops containers, removes volumes, and starts fresh

set -e

echo "🗑️  Stopping containers..."
docker compose down

echo "🗑️  Removing database volumes..."
docker volume rm -f fastapi_lab_postgres_data fastapi_lab_redis_data 2>/dev/null || true

echo "✨ Starting containers with fresh databases..."
docker compose up -d

echo "⏳ Waiting for services to be healthy..."
sleep 5

echo "✅ Done! Databases have been reset."
echo ""
echo "📊 You can check the logs with: docker compose logs -f"
