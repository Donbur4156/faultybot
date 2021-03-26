@echo off
color a 
title Uninstall pip 

pip freeze > del.txt
pip uninstall -r del.txt -y

del del.txt

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

del get-pip.py