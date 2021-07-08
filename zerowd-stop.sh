#!/bin/bash

echo Stopping all watchdogs
killall zerowd.py
killall bcast-recv
sleep 2
killall zerowd.sh

