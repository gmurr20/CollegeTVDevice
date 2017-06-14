#!/bin/bash

#switch to hdmi input 1
echo "tx 4F 82 10 00" | cec-client -s

#turn tv off
echo "standby 0" | cec-client -s

#turn off server
killall -9 python

#kill the browser
killall -9 midori