#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOD_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="${ROOD_DIR}/env/bin/python"

LOCK_FILE=/tmp/NMR_to_openBIS_lock.txt



echo "("$(date +"%T")") Checking for lock file..."

# Check if the lock file exists
if [ -f "$LOCK_FILE" ]; then
  echo "("$(date +"%T")") NMR to openBIS already in progress (Lock file already exists). Terminating script."
  exit 0
fi

echo "("$(date +"%T")") Lock file does not exist. Proceeding with NMR to openBIS..."

# Create the lock file
touch $LOCK_FILE

echo "("$(date +"%T")") Lock file created."

# Execute NMR_to_openBIS script


$PYTHON $ROOD_DIR/src/bode_loader/NMR_to_openBIS.py

echo "("$(date +"%T")") NMR to openBIS script finished"

# Delete the lock file
rm $LOCK_FILE

echo "("$(date +"%T")") Lock file deleted."