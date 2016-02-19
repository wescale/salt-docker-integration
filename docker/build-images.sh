#!/usr/bin/env bash

PWD=`pwd`
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Build minion image
cd ${DIR}/minion
docker build --rm=true --no-cache -t salt-minion .

# Build master image
cd ${DIR}/master
docker build --rm=true --no-cache -t salt-master .

cd ${PWD}
