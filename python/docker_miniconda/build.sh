conda install -n root conda-build anaconda-client

for PYTHON_VERSION in ${PYTHON_VERSIONS}; do
    echo "Building with python ${PYTHON_VERSION}"
    source activate "py${PYTHON_VERSION}"
    cd /code
    conda build .
    source deactivate
done
