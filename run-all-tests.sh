#!/usr/bin/env bash

docker images | grep salt-minion

if [ $? -ne 0 ]; then
    ./docker/build-images.sh
fi

which pip
if [ $? -ne 0 ]; then
    curl https://bootstrap.pypa.io/get-pip.py | sudo python
fi

which virtualenv
if [ $? -ne 0 ]; then
    sudo pip install virtualenv
fi

if [ ! -d .venv ]; then
    virtualenv .venv
    . .venv/bin/activate
    pip install -r requirements.txt --use-wheel
else
    . ./.venv/bin/activate
fi

nose2

