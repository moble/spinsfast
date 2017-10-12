#! /bin/bash

export datetime=$(date +"%Y.%m.%d.%H.%M.%S")
export package_version="104.${datetime}"

python setup.py sdist upload

./python/build_macosx_wheels.sh

open --hide --background -a Docker
while ! (docker ps > /dev/null 2>&1); do
    echo "Waiting for docker to start..."
    sleep 1
done
docker run -i -t \
    -v ${HOME}/.pypirc:/root/.pypirc:ro \
    -v `pwd`:/code \
    -v `pwd`/python/build_manylinux_wheels.sh:/build_manylinux_wheels.sh \
    quay.io/pypa/manylinux1_x86_64 /build_manylinux_wheels.sh "${datetime}"

conda build .
docker build -t manyconda --pull python/docker_miniconda
docker run -i -t \
    -e package_version \
    -v ${HOME}/.condarc:/root/.condarc:ro \
    -v `pwd`:/code \
    manyconda bash -c 'conda build /code'
