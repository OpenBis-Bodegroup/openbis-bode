#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOD_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="${ROOD_DIR}/env/bin/python"

SPACE_STRUCTURE_PATH="${ROOD_DIR}/space_structure.json"
TEST_DIR="${ROOD_DIR}/tests/assets"

$PYTHON -m bode_loader.fetch_space_structure --save_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type TEST --dataset_ab_dir $TEST_DIR --hierarchy "*.txt" "*.pdf" --ab_prefix "BODE - " --space_structure_path $SPACE_STRUCTURE_PATH

rm $SPACE_STRUCTURE_PATH
