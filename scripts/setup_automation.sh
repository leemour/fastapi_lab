#!/bin/bash
# Setup script for automation models

set -e

echo "🚀 Setting up Automation Models..."
echo ""

# 1. Install dependencies
echo "📦 Installing dependencies..."
uv sync
echo "✅ Dependencies installed"
echo ""

# 2. Start PostgreSQL
echo "🐘 Starting PostgreSQL..."
docker-compose up -d postgres
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5
echo "✅ PostgreSQL is running"
echo ""

# 3. Initialize database tables
echo "🗄️  Initializing database tables..."
uv run python scripts/init_tables.py
echo "✅ Database tables created"
echo ""

echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start the application:"
echo "     uvicorn main:app --reload"
echo ""
echo "  2. Visit the API docs:"
echo "     http://localhost:8000/docs"
echo ""
echo "  3. Test the webhook endpoint:"
echo "     curl -X POST http://localhost:8000/v1/webhooks/inbox/test \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"message\": \"Hello from webhook!\"}'"
echo ""
echo "📖 Read AUTOMATION_SUMMARY.md for more examples!"
