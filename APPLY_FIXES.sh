#!/usr/bin/env bash
# Script to apply type: ignore comments to resolve remaining mypy issues

set -e

echo "================================================================"
echo "Applying Type Ignore Fixes for AutoMagik Spark"
echo "================================================================"
echo ""

# Change to script directory
cd "$(dirname "$0")"

echo "Running Python script to apply fixes..."
python3 fix_type_ignores.py

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================"
    echo "✓ All fixes applied successfully!"
    echo "================================================================"
    echo ""
    echo "Now running mypy to verify..."
    echo ""

    if command -v mypy &> /dev/null; then
        mypy .
        echo ""
        echo "================================================================"
        echo "Mypy verification complete."
        echo "================================================================"
    else
        echo "mypy not found. Please run 'mypy .' manually to verify."
    fi
else
    echo ""
    echo "================================================================"
    echo "✗ Some fixes failed. Please review the output above."
    echo "================================================================"
    exit 1
fi
