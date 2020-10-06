#!/usr/bin/bash

pcloud=$(ps aux | grep -i pcloud | grep -v grep | wc -l)
if [ $pcloud -eq 0 ]; then
  exec pcloud 
fi

slack=$(ps aux | grep -i slack | grep -v grep | wc -l)
if [ $slack -eq 0 ]; then
  exec i3-msg 'workspace 6; exec slack'
fi

teams=$(ps aux | grep -i teams | grep -v grep | wc -l)
if [ $teams -eq 0 ]; then
  exec i3-msg 'workspace 6; exec teams'
fi
