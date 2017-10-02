#! /bin/bash

export datetime=$(date +"%Y.%m.%d.%H.%M.%S")
python python/setup.py sdist bdist_wheel upload
source activate py27
python python/setup.py bdist_wheel upload
source deactivate

# open --hide --background -a Docker
# while ! (docker ps > /dev/null 2>&1); do
#     sleep 1
# done
# docker build -t pipify_spinsfast docker

