#!/bin/bash
set -e

echo "🔄 Starting application..."
echo "📍 Current directory: $(pwd)"

# Intentar ejecutar migraciones (puede fallar si no hay DB, es normal)
echo "🗄️  Attempting to run database migrations..."

# Las migraciones están en /app/backend/migrations/, y ese es el WORKDIR
if python -m alembic upgrade head 2>&1 | tee /tmp/migration.log; then
    echo "✅ Migrations completed successfully"
else
    echo "⚠️  Migration warning (this is normal on first startup)"
    echo "   Full log: $(cat /tmp/migration.log | head -20)"
fi

echo "🚀 Starting FastAPI server..."
exec "$@"
