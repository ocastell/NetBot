#!/bin/bash
pipe=$1
IP_NETBOT=$2
AUDIO_PORT=$3

if [[ ! -p $pipe ]]; then
    mkfifo $pipe
fi

while true
do
    #echo "Press and hold [CTRL+C] to stop.."
    #echo "IP_NETBOT..",$IP_NETBOT
    #echo "AUDIO_PORT..",$AUDIO_PORT
    netcat -v $IP_NETBOT $AUDIO_PORT > $pipe
done
