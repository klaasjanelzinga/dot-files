#!/usr/bin/env bash

while [ 0 ]; do
  file=$(find ~/pCloudDrive/klaasjan/pics/desktop/*.png |sort -R |tail -1)
  feh -q --bg-scale $file
  sleep 360
done
# export I3SOCK=$(ls /run/user/1000/sway-ipc.1000.*.sock)
# swaymsg output "*"  bg $file fill
