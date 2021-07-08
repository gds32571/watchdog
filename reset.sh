#!/bin/bash

echo Resetting all watchdog counters


./reset.py 3001
./reset.py 3007 
./reset.py 3009
./reset.py 3011
./reset.py 3020
./reset.py 3021
./reset.py 3022
./reset.py 3023
./reset.py 3024
./reset.py 3025

echo Done!
