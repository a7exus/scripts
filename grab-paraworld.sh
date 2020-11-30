#!/bin/bash

DIR=/home/pi/tmp/paraworld
D=`date '+%Y.%m.%d-%H:%M'`
F_EN=$DIR/en-$D
EN_LAST_MD5=$(md5sum $(ls -rt $DIR/en-* | tail -1) | cut -f1 -d\ )
F_DE=$DIR/de-$D
DE_LAST_MD5=$(md5sum $(ls -rt $DIR/de-* | tail -1) | cut -f1 -d\ )

HUA='user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
HREF='referer: https://www.paraworld.ch/en/'

curl -s -o "$F_DE" -H "$HUA" -H "$HREF" https://www.paraworld.ch/gleitschirm-schule-zentralschweiz
curl -s -o "$F_EN" -H "$HUA" -H "$HREF" https://www.paraworld.ch/en/tagesprogramm/

EN_MD5=$(md5sum $F_EN | cut -f1 -d\ )
DE_MD5=$(md5sum $F_DE | cut -f1 -d\ )

[ $EN_MD5 == $EN_LAST_MD5 ] && rm "$F_EN"
[ $DE_MD5 == $DE_LAST_MD5 ] && rm "$F_DE"

