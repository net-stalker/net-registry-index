#!/bin/bash

# Change directory to the tests directory
cd scripts/tests

# Loop through all Python files and run them
for file in *.py; do
    if [[ -f "$file" ]]; then
        echo "Running $file..."
        python "$file"
    fi
done

