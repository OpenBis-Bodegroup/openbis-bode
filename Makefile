.PHONY: test python # these are not real files

python=./env/bin/python

all: env

env:
	conda env create -f ./environment.yaml -p ./env

# before this step please install java 17
build-openbis:
	git clone https://sissource.ethz.ch/sispub/openbis.git openbis.git --depth 1
	cd openbis.git/app-openbis-installer/ && ./gradlew clean && ./gradlew build -x test "-Dorg.gradle.jvmargs=--add-opens=java.base/java.text=ALL-UNNAMED --add-opens=java.desktop/java.awt.font=ALL-UNNAMED"
	cd openbis.git/api-openbis-javascript/ && ./gradlew clean && ./gradlew bundleOpenbisStaticResources -x test
	${python} -m pip install --upgrade pybis
