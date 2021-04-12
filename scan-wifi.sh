#!/bin/bash

sudo iwlist wlan0 scan | grep -e ESSID -e Address -e Channel:  -e level= | sed  'N; N; N; s/\n                    / /g;' | grep -v -e Koala -e UPC3250543 -e 'UPC Wi-Free' | ts '[%Y-%m-%d %H:%M:%S]'
