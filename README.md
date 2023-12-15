# OpenBIS Bode group prototying project

In this prototyping session, we prototype a compact experiment registration workflow. The important steps are:
1. automatic insertion of the experimental data into the openBIS database, on data generation
2. automatic registration of the compact experiment, when data is uploaded to openBIS
3. enable preview of the data in the openBIS web interface

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
    - `Bode - {USER_ETH_ID_UPPER_CASE}-{PROJECT_NAME_UPPER_CASE}-{EXPERIMENT_NAME_UPPER_CASE}-{DESCRIPTION}`
    - USER_ETH_ID: ETH ID of the user, upper case
    - PROJECT_NAME: name of the project that the user made in openbis, upper case
    - EXPERIMENT_NAME: name of the experiment that the user made in openbis, upper case
    - DESCRIPTION: description of the data, does not need to be upper case

## TODO
- [ ] Connection to the data server should be fixed, at the moment, manually connect to the server from PC then use that path as the data path to the data server.
- [ ] User listing is not ideal at the moment.
