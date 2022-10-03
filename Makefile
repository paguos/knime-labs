NODE = penguin
CONDA_ENV = knime-labs-${NODE}-env
BUILD_ENV = knime-ext-bundling

create/conda:
	conda env create  -f ${NODE}/environment.yml   

create/builder:
	conda create -n ${BUILD_ENV} -c knime -c conda-forge knime-extension-bundling   

lint:
	conda run --name ${CONDA_ENV} --cwd ${NODE} flake8

unit:
	conda run --name ${CONDA_ENV} --cwd ${NODE} pytest

tests: lint unit

build: tests
	conda run --name ${BUILD_ENV} build_python_extension.py ${NODE} build_${NODE}
