# OpenBIS Bode group prototying project

In this prototyping session, we prototype a compact experiment registration workflow. The important steps are:
1. automatic insertion of the experimental data into the openBIS database, on data generation
2. automatic registration of the compact experiment, when data is uploaded to openBIS
3. enable preview of the data in the openBIS web interface

The main documentation is here: https://openbis.readthedocs.io/en/latest/software-developer-documentation/apis/python-v3-api.html

## Setup
1. Install java 17: https://www.oracle.com/java/technologies/downloads/#java17
2. setup environment with make
    ```
    make env
    conda activate ./env
    make build-openbis
    ```
