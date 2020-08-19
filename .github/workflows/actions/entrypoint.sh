#!/bin/sh

yum install -y fftw3 fftw3-devel

PYTHONS=("cp36-cp36m" "cp37-cp37m" "cp38-cp38")

for PYTHON in ${PYTHONS[@]}; do
    /opt/python/${PYTHON}/bin/pip install --upgrade pip wheel auditwheel
    /opt/python/${PYTHON}/bin/pip install -r ./python/dev-requirements.txt
    /opt/python/${PYTHON}/bin/pip wheel ./ -w /github/workspace/wheelhouse/
done

for whl in /github/workspace/wheelhouse/*.whl; do
    auditwheel repair $whl
done
