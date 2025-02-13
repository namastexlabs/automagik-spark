
#!/bin/bash

# Drop and recreate database
PGPASSWORD=automagik psql -h localhost -U automagik -d postgres -c "DROP DATABASE IF EXISTS automagik;"
PGPASSWORD=automagik psql -h localhost -U automagik -d postgres -c "CREATE DATABASE automagik;"

# Remove all migration versions
rm -f /root/automagik/migrations/versions/*.py

# Initialize fresh migrations
cd /root/automagik
/root/automagik/.venv/bin/alembic revision --autogenerate -m "initial"
/root/automagik/.venv/bin/alembic upgrade head


