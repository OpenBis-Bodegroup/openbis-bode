#!/bin/bash

COMPACT_DIR=PATH_TO_COMPACT_DIR
MALDI_DIR1=PATH_TO_MALDI_DIR
MALDI_DIR2=PATH_TO_MALDI_DIR
AMAZON_LCMS_DIR=PATH_TO_AMAZON_LCMS_DIR
AGILENT_LCMS_DIR1=PATH_TO_AGILENT_LCMS_DIR
AGILENT_LCMS_DIR2=PATH_TO_AGILENT_LCMS_DIR
AGILENT_GCMS_DIR=PATH_TO_AGILENT_GCMS_DIR
HPLC_DIR1=PATH_TO_HPLC_DIR
HPLC_DIR2=PATH_TO_HPLC_DIR
HPLC_DIR3=PATH_TO_HPLC_DIR
HPLC_DIR4=PATH_TO_HPLC_DIR
HPLC_DIR5=PATH_TO_HPLC_DIR
IR_DIR=PATH_TO_IR_DIR
COMPACT_REPRO_DIR=PATH_TO_COMPACT_REPRO_DIR

python scripts/upload_data.py --dataset_type COMPACT --dataset_ab_dir $COMPACT_DIR --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
python scripts/upload_data.py --dataset_type MALDI --dataset_ab_dir $MALDI_DIR1 --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
python scripts/upload_data.py --dataset_type MALDI --dataset_ab_dir $MALDI_DIR2 --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
python scripts/upload_data.py --dataset_type AMAZON-LCMS --dataset_ab_dir $AMAZON_LCMS_DIR --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
python scripts/upload_data.py --dataset_type AGILENT-LCMS --dataset_ab_dir $AGILENT_LCMS_DIR1 --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode_"
python scripts/upload_data.py --dataset_type AGILENT-LCMS --dataset_ab_dir $AGILENT_LCMS_DIR2 --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode_"
python scripts/upload_data.py --dataset_type AGILENT-GCMS --dataset_ab_dir $AGILENT_GCMS_DIR --hierarchy "*/pdf/*.pdf" --ab_prefix "Bode - "
python scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR1 --hierarchy "**/*.pdf" --ab_prefix ""
python scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR2 --hierarchy "**/*.pdf" --ab_prefix ""
python scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR3 --hierarchy "**/*.pdf" --ab_prefix ""
python scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR4  --hierarchy "**/*.pdf" --ab_prefix ""
python scripts/upload_data.py --dataset_type HPLC --dataset_ab_dir $HPLC_DIR5 --hierarchy "**/*.pdf" --ab_prefix ""
python scripts/upload_data.py --dataset_type IR --dataset_ab_dir $IR_DIR --hierarchy "**/*.pdf" --ab_prefix ""
python scripts/upload_data.py --dataset_type COMPACT-REPRO --dataset_ab_dir $COMPACT_REPRO_DIR --hierarchy "*/data_preprocessed/*" --ab_prefix "Bode - "
