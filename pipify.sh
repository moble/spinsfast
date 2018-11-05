#! /bin/bash

export datetime=$(date +"%Y.%m.%d.%H.%M.%S")

python setup.py sdist upload

./python/build_macosx_wheels.sh ${datetime}

# open --hide --background -a Docker
# while ! (docker ps > /dev/null 2>&1); do
#     echo "Waiting for docker to start..."
#     sleep 1
# done
# docker run -i -t \
#     -v ${HOME}/.pypirc:/root/.pypirc:ro \
#     -v `pwd`:/code \
#     -v `pwd`/python/build_manylinux_wheels.sh:/build_manylinux_wheels.sh \
#     quay.io/pypa/manylinux1_x86_64 /build_manylinux_wheels.sh "${datetime}"
