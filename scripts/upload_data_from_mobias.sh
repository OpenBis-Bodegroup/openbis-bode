#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOD_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="${ROOD_DIR}/env/bin/python"

COMPACT_DIR="/Volumes/Bode/Bruker-Compact-1"
MALDI_DIR1="/Volumes/Bode/Bruker-Microflex-1"
MALDI_DIR2="/Volumes/Bode/Bruker-Microflex-2"
AMAZON_LCMS_DIR="/Volumes/Bode/Bruker-Amazon-1"
AGILENT_LCMS_DIR1="/Volumes/Bode/Agilent-G6120C-1"
AGILENT_LCMS_DIR2="/Volumes/Bode/Agilent-G6135C-1"
AGILENT_GCMS_DIR="/Volumes/Bode/Agilent-GC-5975-MSD-1"
HPLC_DIR1="/Volumes/chab_loc_bode_s1/Instruments/HPLC reversed phase F316"
HPLC_DIR2="/Volumes/chab_loc_bode_s1/Instruments/HPLC reversed phase F310 (former F316)"
HPLC_DIR3="/Volumes/chab_loc_bode_s1/Instruments/HPLC reversed phase automated:SEC F318"
HPLC_DIR4="/Volumes/chab_loc_bode_s1/Instruments/HPLC reversed phase F318"
HPLC_DIR5="/Volumes/chab_loc_bode_s1/Instruments/HPLC Dionex"
IR_DIR="/Volumes/chab_loc_bode_s1/Instruments/IR/Current data (backup)/Bode group"
COMPACT_REPRO_DIR="/Volumes/Bode/Bruker-Compact-1-Repro"

$PYTHON scripts/upload_data.py --dataset_type COMPACT --dataset_ab_dir $COMPACT_DIR --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
$PYTHON scripts/upload_data.py --dataset_type MALDI --dataset_ab_dir $MALDI_DIR1 --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
$PYTHON scripts/upload_data.py --dataset_type MALDI --dataset_ab_dir $MALDI_DIR2 --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
$PYTHON scripts/upload_data.py --dataset_type AMAZON-LCMS --dataset_ab_dir $AMAZON_LCMS_DIR --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
$PYTHON scripts/upload_data.py --dataset_type AGILENT-LCMS --dataset_ab_dir $AGILENT_LCMS_DIR1 --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode_"
$PYTHON scripts/upload_data.py --dataset_type AGILENT-LCMS --dataset_ab_dir $AGILENT_LCMS_DIR2 --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode_"
$PYTHON scripts/upload_data.py --dataset_type AGILENT-GCMS --dataset_ab_dir $AGILENT_GCMS_DIR --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
$PYTHON scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR1 --hierarchy "**/*.pdf" --ab_prefix ""
$PYTHON scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR2 --hierarchy "**/*.pdf" --ab_prefix ""
$PYTHON scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR3 --hierarchy "**/*.pdf" --ab_prefix ""
$PYTHON scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR4  --hierarchy "**/*.pdf" --ab_prefix ""
$PYTHON scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR5 --hierarchy "**/*.pdf" --ab_prefix ""
$PYTHON scripts/upload_data.py --dataset_type IR --dataset_ab_dir $IR_DIR --hierarchy "**/*.pdf" --ab_prefix ""
$PYTHON scripts/upload_data.py --dataset_type COMPACT-REPRO --dataset_ab_dir $COMPACT_REPRO_DIR --hierarchy "*/data_preprocessed/*" --ab_prefix "Bode - "
