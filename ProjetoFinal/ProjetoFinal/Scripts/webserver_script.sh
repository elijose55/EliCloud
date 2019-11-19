#!/bin/sh

cd CloudComputing
cd ProjetoFinal
cd aps1
sudo apt install python3-pip
export LC_ALL=C
pip3 install flask
pip3 install flask_restful
pip3 install flask_httpauth
pip3 install jsonpickle
python3 aps1.py



