#!/bin/bash


xset +dpms
xset s on
xautolock -enable

# brightness
max=$(brightnessctl m)
brightnessctl s $max

amixer -q sset Capture 100%
amixer set Master 100%
