#!/bin/bash

if [ ! -d ./.venv/ ];
then
    python3 -m venv ./.venv/ && . ./.venv/bin/activate
    python -m pip install pip --upgrade
    python -m pip install -r ./requirements.txt    

else
    . ./.venv/bin/activate
    python -m pip install -r ./requirements.txt
fi

python -m jupyter notebook ./ --ip=127.0.0.1 --port=8888
