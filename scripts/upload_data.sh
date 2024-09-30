#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON="${ROOT_DIR}/env/bin/python"
SPACE_STRUCTURE_PATH="${ROOT_DIR}/space_structure.json"

COMPACT_DIR="/Volumes/chab_mobias_oadata/OpenAccess/DCHAB/LOC/Bode"
COMPACT_REPRO_DIR="/Volumes/chab_mobias_oadata/OpenAccess/DCHAB/LOC/Bode/Bruker-Compact-1-Repro"
MALDI_DIR="/Volumes/chab_mobias_oadata/OpenAccess/DCHAB/LOC/Bode"
AMAZON_LCMS_DIR="/Volumes/chab_mobias_oadata/OpenAccess/DCHAB/LOC/Bode/Bruker-Amazon-1"
AGILENT_LCMS_DIR="/Volumes/chab_mobias_oadata/OpenAccess/DCHAB/LOC/Bode"
AGILENT_GCMS_DIR="/Volumes/chab_mobias_oadata/OpenAccess/DCHAB/LOC/Bode/Agilent-GC-5975-MSD-1"
HPLC_DIR="/Volumes/chab_loc_bode_s1/Instruments"
IR_DIR="/Volumes/chab_loc_bode_s1/Instruments/IR/Current data (backup)/Bode group"
GEL_SCAN_DIR="/Volumes/chab_loc_bode_s1/Instruments/ChemiDoc Gel Scanner"
NANODROP_DIR="/Volumes/chab_loc_bode_s1/Instruments/NanoDrop"
PLATE_READER_DIR="/Volumes/chab_loc_bode_s1/Instruments/Plate reader"
POLARIMETER_DIR="/Volumes/chab_loc_bode_s1/Instruments/Polarimeter/Current data (backup)/Bode group"
NMR_DIR="/Volumes/chab_loc_bode_s1/Instruments/NMR/NMRtoOpenBIS"
SYMPHONY_DIR="/Volumes/chab_loc_bode_s1/Instruments/Symphony_X"
KNAUER_HPLC_DIR="/Volumes/chab_loc_bode_s1/Instruments/HPLC Knauer/Data/ETH"

# Fetch space structure
$PYTHON -m bode_loader.fetch_space_structure --save_path $SPACE_STRUCTURE_PATH

# Upload data
# TODO: In the future, if following process gets too slow,
# 1) we can parallelize the upload process by running each upload command in a separate process.
#    search 'parallel bash forloop'
# 2) discuss with openbis team to implement a more efficient way to upload data (or faster fetch api).
$PYTHON -m bode_loader.upload_data --dataset_type COMPACT --dataset_ab_dir $COMPACT_DIR --hierarchy "Bruker-Compact-1/*/pdf/*.pdf" "Bruker-Compact-2/*/pdf/*.pdf" --ab_prefix "Bode - " --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type COMPACT-REPRO --dataset_ab_dir $COMPACT_REPRO_DIR --hierarchy "*/data_reprocessed/*" --ab_prefix "Bode - " --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type MALDI --dataset_ab_dir $MALDI_DIR --hierarchy "Bruker-Microflex-1/*/pdf/*.pdf" "Bruker-Microflex-2/*/pdf/*.pdf" --ab_prefix "Bode - " --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type AMAZON-LCMS --dataset_ab_dir $AMAZON_LCMS_DIR --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - " --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type AGILENT-LCMS --dataset_ab_dir $AGILENT_LCMS_DIR --hierarchy "Agilent-G6120C-1/*/pdf/*.pdf" "Agilent-G6135C-1/*/pdf/*.pdf" --ab_prefix "Bode_"  --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type AGILENT-GCMS --dataset_ab_dir $AGILENT_GCMS_DIR --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - " --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type HPLC --dataset_ab_dir "${HPLC_DIR}" --hierarchy "HPLC reversed phase F310 (former F316)/HPLC data synchronized/**/*.pdf" "HPLC reversed phase F310 (former F316)/HPLC data synchronized/**/*.png" "HPLC reversed phase F316/HPLC Data/**/*.pdf" "HPLC reversed phase F316/HPLC Data/**/*.png" "HPLC reversed phase automated:SEC F318/Exported data/**/*.pdf" "HPLC reversed phase automated:SEC F318/Exported data/**/*.png" "HPLC reversed phase F318/Exported data/**/*.pdf" "HPLC reversed phase F318/Exported data/**/*.png" "HPLC Dionex/**/*.pdf" "HPLC Dionex/**/*.png" --ab_prefix "" --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type HPLC_RAW --dataset_ab_dir "${HPLC_DIR}" --hierarchy "HPLC reversed phase F310 (former F316)/HPLC data synchronized/**/*.csv" "HPLC reversed phase F316/HPLC Data/**/*.csv" "HPLC reversed phase automated:SEC F318/Exported data/**/*.csv" "HPLC reversed phase F318/Exported data/**/*.csv" "HPLC Dionex/**/*.csv" --ab_prefix "" --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type IR --dataset_ab_dir "${IR_DIR}" --hierarchy "**/*.pdf" --ab_prefix "" --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type NANODROP --dataset_ab_dir "${NANODROP_DIR}" --hierarchy "**/*.pdf" --ab_prefix "" --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type GEL_SCAN --dataset_ab_dir "${GEL_SCAN_DIR}" --hierarchy "*/ChemiDoc Images 2024*/*.jpg" "*/ChemiDoc Images 2024*/*.scn" --ab_prefix ""  --space_structure_path $SPACE_STRUCTURE_PATH #The year needs to be changed according to the current year. Please don't forget :)
$PYTHON -m bode_loader.upload_data --dataset_type PLATE_READER --dataset_ab_dir "${PLATE_READER_DIR}" --hierarchy "**/*.xlsx" --ab_prefix "" --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type POLARIMETER --dataset_ab_dir "${POLARIMETER_DIR}" --hierarchy "**/*.txt" --ab_prefix "" --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type NMR_RAW --dataset_ab_dir "${NMR_DIR}" --hierarchy "*.zip" --ab_prefix "" --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type SPPS_REPORT --dataset_ab_dir "${SYMPHONY_DIR}" --hierarchy "Exported_Reports/*.pdf" --ab_prefix "SYNTHESIS-" --space_structure_path $SPACE_STRUCTURE_PATH
$PYTHON -m bode_loader.upload_data --dataset_type KNAUER-HPLC --dataset_ab_dir "${KNAUER_HPLC_DIR}" --hierarchy "**/*.pdf" --ab_prefix "" --space_structure_path $SPACE_STRUCTURE_PATH

# Remove space structure
rm $SPACE_STRUCTURE_PATH
