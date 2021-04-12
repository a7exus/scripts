#!/bin/bash

D=/run/user/1000/dump1090/data/
mkdir -p $D
chmod +rx /run/user/1000

echo "Enabling bias_tee:"
(cd /home/pi/sdr/rtl_biast/build/src/; ./rtl_biast -b 1;)

echo "Starting screen..."
screen -d -m /home/pi/sdr/dump1090/dump1090 --gain -10 --lat 0 --lon 0 --write-json $D --quiet
