#!/bin/bash -e

#serverIP=$1

gst-launch-1.0 -v udpsrc port=5500 caps="application/x-rtp" ! queue ! rtppcmudepay ! mulawdec ! audioconvert ! autoaudiosink sync=false &

#gst-launch-1.0 -v tcpclientsrc host=$serverIp port=5000 ! gdpdepay ! rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false

kill $!
