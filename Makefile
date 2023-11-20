.PHONY: test python # these are not real files

python=./env/bin/python

all: env

env:
	conda env create -f ./environment.yaml -p ./env
