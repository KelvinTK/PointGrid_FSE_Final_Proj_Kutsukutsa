#!/bin/bash

wget http://modelnet.cs.princeton.edu/ModelNet40.zip
unzip ModelNet40.zip
./prepare.py
./setup.py
