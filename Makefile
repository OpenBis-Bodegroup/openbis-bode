.PHONY: test python # these are not real files

python=./env/bin/python

all: env

env:
	conda env create -f ./environment.yaml -p ./env
	${python} -m pip install -e .

fetch-space-structure:
	${python} -m bode_loader.fetch_space_structure

upload-data:
	${python} -m bode_loader.upload_data ${ARGS}

test:
	${python} -m pytest tests/
