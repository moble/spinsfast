#!/bin/sh

yum install -y fftw3 fftw3-devel

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/

PYTHONS=("cp36-cp36m" "cp37-cp37m" "cp38-cp38" "cp39-cp39")

for PYTHON in ${PYTHONS[@]}; do
    /opt/python/${PYTHON}/bin/pip install --upgrade pip wheel auditwheel
    /opt/python/${PYTHON}/bin/pip install -r ./python/dev-requirements.txt
    /opt/python/${PYTHON}/bin/pip wheel ./ -w /github/workspace/wheelhouse/
done

for whl in /github/workspace/wheelhouse/*.whl; do
    auditwheel repair $whl
done
