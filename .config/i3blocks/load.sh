#!/bin/bash

load_now="$(cut -d ' ' -f1 /proc/loadavg)"
load_10="$(cut -d ' ' -f2 /proc/loadavg)"
load_15="$(cut -d ' ' -f3 /proc/loadavg)"
case $BLOCK_BUTTON in
  1)
    statusLine=$(cat /proc/loadavg)
    ;;
  3)
    statusLine=$(uptime)
    ;;
  *)
    statusLine=$load_now
    ;;
esac

red='"red"'
white='"white"'
orange='"orange"'

if [ 1 -eq "$(echo "${load_now} > $(nproc)" | bc)" ]
then
  echo "<span foreground=$white><b>🖥  $statusLine</b></span>"
  exit 33
fi
if [ 1 -eq "$(echo "${load_now} > $(nproc)/2" | bc)" ]
then
  echo "<span foreground=$red><b>🖥  $statusLine</b></span>"
  exit 0
fi
if [ 1 -eq "$(echo "${load_now} > $(nproc)/3" | bc)" ]
then
  echo "<span foreground=$orange><b>🖥  $statusLine</b></span>"
  exit 0
fi

echo "🖥 $statusLine"
exit 0

