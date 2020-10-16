#!/usr/bin/bash

export DISPLAY=:0
pcloud=$(ps aux | grep -i pcloud | grep -v grep | wc -l)
if [ $pcloud -eq 0 ]; then
  i3-msg 'exec pcloud'
fi

slack=$(ps aux | grep -i slack | grep -v grep | wc -l)
if [ $slack -eq 0 ]; then
  i3-msg 'exec slack'
  sleep 3
  i3-msg '[class="Slack"] move to workspace "6"'
fi

teams=$(ps aux | grep -i teams | grep -v grep | wc -l)
if [ $teams -eq 0 ]; then
  i3-msg 'exec teams'
  sleep 5
  i3-msg '[class="Microsoft Teams - Preview"] move to workspace "6"'
fi
