#!/bin/bash

case $BLOCK_BUTTON in
  2)
    max=$(brightnessctl m)
    statusLine=$(brightnessctl g)
    if [ "$statusLine" == "0" ]; then
      res=$(brightnessctl s $max)
    else
      res=$(brightnessctl s 0)
    fi
    ;;
  1 | 4)
    res=$(brightnessctl s 4%+)
    ;;
  3 | 5)
    res=$(brightnessctl s 4%-)
    ;;
  *)
    ;;
esac

statusLine=$(brightnessctl g)
if [ "$statusLine" == "0" ]; then
  statusLine="off"
fi


echo "🌞 ${statusLine}"
