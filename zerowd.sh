#!/bin/bash

echo Stopping all watchdogs
killall zerowd.py
killall bcast-recv
sleep 5

echo Starting database
./zerowd.py 99 &

echo Starting bcast receiver
./bcast-recv &

sleep 5

echo Starting watchdogs

./zerowd.py 1 &
#./zerowd.py 2 &
#./zerowd.py 3 &
#./zerowd.py 4 &
#./zerowd.py 5 &
./zerowd.py 6 &
#./zerowd.py 7 &
./zerowd.py 8 &
./zerowd.py 9 &
./zerowd.py 10 &
#./zerowd.py 11 &

./zerowd.py 20 &
./zerowd.py 21 &
./zerowd.py 22 &
./zerowd.py 23 &
./zerowd.py 24 &
./zerowd.py 25 &
./zerowd.py 26 &


$SHELL
