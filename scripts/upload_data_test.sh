#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOD_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="${ROOD_DIR}/env/bin/python"

TEST_DIR="${ROOD_DIR}/tests/assets"

$PYTHON -m bode_loader.upload_data --dataset_type TEST --dataset_ab_dir $TEST_DIR --hierarchy "*.txt" "*.pdf" --ab_prefix "BODE - "
