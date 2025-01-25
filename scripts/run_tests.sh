#!/bin/bash
set -e

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run tests with coverage
python -m pytest -v tests/ --cov=automagik --cov-report=term-missing

# Check test coverage threshold
coverage_threshold=45
coverage_result=$(coverage report | grep "TOTAL" | awk '{print $4}' | sed 's/%//')

if awk "BEGIN {exit !($coverage_result < $coverage_threshold)}"; then
    echo "❌ Test coverage ($coverage_result%) is below the required threshold ($coverage_threshold%)"
    exit 1
fi

echo "✅ All tests passed with coverage $coverage_result%"
exit 0
