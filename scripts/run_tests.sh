
#!/bin/bash
set -e

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run tests with coverage
python -m pytest tests/

# Check test coverage threshold
coverage_result=$(coverage report | grep "TOTAL" | awk '{print $4}' | sed 's/%//')
coverage_threshold=45

if (( $(echo "$coverage_result < $coverage_threshold" | bc -l) )); then
    echo " Test coverage ($coverage_result%) is below the required threshold ($coverage_threshold%)"
    exit 1
fi

echo " All tests passed with coverage $coverage_result%"
exit 0


