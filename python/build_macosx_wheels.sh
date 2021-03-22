#! /bin/bash
set -e
set -x

. ~/.continuum/anaconda3/etc/profile.d/conda.sh
conda activate base

export package_version="${1:-$(date +'104.%Y.%m.%d.%H.%M.%S')}"
echo "Building macosx wheels, version '${package_version}'"

temp_dir="${HOME}/Research/Temp"
wheelhouse="${temp_dir}/wheelhouse"
code_dir="${PWD}"

/bin/rm -rf "${wheelhouse}"
mkdir -p "${wheelhouse}"

CONDA_ENVS=( py27 py36 py37 py38 py39 )

# Update conda envs
for CONDA_ENV in "${CONDA_ENVS[@]}"; do
    conda activate "${CONDA_ENV}"
    conda update -y --all
    conda install -y fftw
    pip install --upgrade pip
    conda deactivate
done

# Compile wheels
for CONDA_ENV in "${CONDA_ENVS[@]}"; do
    conda activate "${CONDA_ENV}"
    ### NOTE: The path to the requirements file is specialized for spinsfast
    pip install -r ./python/dev-requirements.txt
    pip wheel ./ -w "${wheelhouse}/"
    conda deactivate
done

# Bundle external shared libraries into the wheels
for whl in $(ls $(echo "${wheelhouse}/*.whl")); do
    echo
    delocate-listdeps --depending "$whl"
    delocate-wheel -v "$whl"
    delocate-listdeps --depending "$whl"
    echo
done


### NOTE: These lines are specialized for spinsfast
for CONDA_ENV in "${CONDA_ENVS[@]}"; do
    conda activate "${CONDA_ENV}"
    # Install packages and test ability to import and run simple command
    pip install --upgrade spinsfast --no-index -f "${wheelhouse}"
    (cd "$HOME"; python -c 'import spinsfast; print(spinsfast.__version__); print("N_lm(8) = {0}".format(spinsfast.N_lm(8)))')
    conda deactivate
done


# Upload to pypi
pip install twine
twine upload "${wheelhouse}"/*macosx*.whl
