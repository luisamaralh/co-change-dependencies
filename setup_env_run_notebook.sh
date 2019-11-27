#!/bin/bash

if ! [ -f /home/user/my_file ];
then
    python3 -m venv ./pyenv/ && . ./pyenv/bin/activate
    python -m pip install -r ./requirements.txt    

else
    . ./pyenv/bin/activate
    python -m pip install -r ./requirements.txt
fi

python -m jupyter notebook ./ --ip=127.0.0.1 --port=8888