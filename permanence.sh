#!/bin/bash

red () {
	echo -e "\e[41m$*\e[49m";
}

notif () {
	notify-send --urgency=critical "
	====================================
	====================================
	====================================
	====================================
	====================================
	===============  $1  ===============
	====================================
	====================================
	====================================
	====================================
	===================================="
}

while :
do
	OLDN="$N"
	N=$(curl -s https://permanence.ch/index.php/ticketprinter/index | grep ticketnummer | grep -oP '(?<=>)\d+(?=<)')
	[ "$N" == "$OLDN" ] && echo -n '.' || echo -e '\n' $N
	[ "$N" -gt 66 ] && red $N
	[ "$N" -gt 66 ] && notif "$N"
	sleep 15
done