#!/bin/bash
# Wait for Postgres to be ready before executing the next command

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for Postgres at $host..."

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -c '\q'; do
  echo "Postgres is unavailable - sleeping 1 second"
  sleep 1
done

echo "Postgres is up - executing command: $cmd"
exec $cmd
