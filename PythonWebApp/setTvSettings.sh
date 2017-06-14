#!/bin/bash

#turn tv on
echo "on 0" | cec-client -s

#switch to hdmi input 2
echo "tx 4F 82 10 00" | cec-client -s