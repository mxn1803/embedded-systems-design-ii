#!/bin/bash

python3 sniffer/sniffer.py > /dev/null 2>&1 &

cd app
npm start