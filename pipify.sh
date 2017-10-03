#! /bin/bash

export datetime=$(date +"%Y.%m.%d.%H.%M.%S")
python setup.py sdist bdist_wheel upload
source activate py27
python setup.py bdist_wheel upload
source deactivate

open --hide --background -a Docker
while ! (docker ps > /dev/null 2>&1); do
    sleep 1
done
docker run -i -t \
    -v ${HOME}/.pypirc:/root/.pypirc:ro \
    -v `pwd`:/code \
    -v `pwd`/python/build_manylinux_wheels.sh:/build_manylinux_wheels.sh \
    quay.io/pypa/manylinux1_x86_64 /build_manylinux_wheels.sh "${datetime}"


# docker build -t pipify_spinsfast docker
# docker run -v ${HOME}/.pypirc:/var/www/.pypirc:ro -v ${PWD}:/var/www/spinsfast -i -t pipify_spinsfast

# cd /var/www/spinsfast && python setup.py bdist_wheel
