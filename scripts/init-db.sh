#!/bin/bash
# Database initialization script

set -e

echo "Starting database initialization..."

# First, create the main databases if they don't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    -- Create main application database if it doesn't exist
    SELECT 'CREATE DATABASE fastapi_lab'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fastapi_lab')\gexec

    -- Create test database if it doesn't exist
    SELECT 'CREATE DATABASE fastapi_lab_test'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'fastapi_lab_test')\gexec

    -- Grant permissions
    GRANT ALL PRIVILEGES ON DATABASE fastapi_lab TO $POSTGRES_USER;
    GRANT ALL PRIVILEGES ON DATABASE fastapi_lab_test TO $POSTGRES_USER;
EOSQL

# Install extensions in the main database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "fastapi_lab" <<-EOSQL
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    CREATE EXTENSION IF NOT EXISTS "btree_gin";
EOSQL

# Install extensions in the test database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "fastapi_lab_test" <<-EOSQL
    -- Create extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pg_trgm";
    CREATE EXTENSION IF NOT EXISTS "btree_gin";
EOSQL

echo "Database initialization completed successfully!"
