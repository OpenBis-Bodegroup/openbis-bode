# OpenBIS Bode group data registration

**THIS REPOSITORY IS ARCHIVED ON 5TH APR 2024, PLEASE RECIRECT TO https://github.com/OpenBis-Bodegroup/openbis-bode**

This repository contains the code to register & synchronize data in openBIS by connecting to the raw data in the Bode group & external ETH servers.

Main functionalities:
1. Fetch User-Project-Experiment structure from openBIS: [fetch_space_structure.py](src/bode_loader/fetch_space_structure.py)
2. Fetch data from the Bode group (and other data storage) servers and upload the new data to openBIS: [upload_data.py](src/bode_loader/upload_data.py)
3. Transform NMR data to a format that can be uploaded to openBIS: [NMR_to_openBIS.py](src/bode_loader/NMR_to_openBIS.py)

For the regular registration of the data, the scripts, [upload_data.sh](scripts/upload_data.sh) and [crontab_helper_NMR.sh](scripts/crontab_helper_NMR.sh), are used and are run as cron jobs on the server.

The main documentation is here: https://openbis.readthedocs.io/en/latest/software-developer-documentation/apis/python-v3-api.html

## Setup
setup environment with make
```
make env
conda activate ./env
```

## Important notes
- Data name should follow the convention:
    - Please no not use '-' and '.' in any of the names, as this is used as a separator
    - `Bode - {USER_ETH_ID_UPPER_CASE}-{PROJECT_CODE_UPPER_CASE}-{EXPERIMENT_CODE_UPPER_CASE}-{DESCRIPTION}`
    - USER_ETH_ID: ETH ID of the user, upper case
    - PROJECT_CODE: code of the project that the user made in openbis, upper case
    - EXPERIMENT_CODE: code of the experiment that the user made in openbis, upper case
    - DESCRIPTION: description of the data, does not need to be upper case
