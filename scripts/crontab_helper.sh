#!/bin/bash

LOCK_FILE=/tmp/upload_data_lock.txt
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "("$(date +"%T")") Checking for lock file..."

# Check if the lock file exists
if [ -f "$LOCK_FILE" ]; then
  echo "("$(date +"%T")") Data upload already in progress (Lock file already exists). Terminating script."
  exit 0
fi

echo "("$(date +"%T")") Lock file does not exist. Proceeding with data upload..."

# Create the lock file
touch $LOCK_FILE

echo "("$(date +"%T")") Lock file created."

# Execute upload_data script
bash "${SCRIPT_DIR}/upload_data.sh"

echo "("$(date +"%T")") upload_data script finished"

# Delete the lock file
rm $LOCK_FILE

echo "("$(date +"%T")") Lock file deleted."
