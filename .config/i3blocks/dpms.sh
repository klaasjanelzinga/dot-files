#!/bin/bash

DPMS_DISABLED=$(xset q | grep "DPMS is Disabled" | awk '{ print $3}' )

case $BLOCK_BUTTON in
  1)
    xset +dpms
    xset s on
    xautolock -enable
    echo "🌷 DPMS enabled" 
    exit 0
    ;;
  2)
    if [ "$DPMS_DISABLED" == "Disabled" ]; then
      xset +dpms
      xset s on
      xautolock -enable
    else
      xset -dpms
      xset s off
      xautolock -disable
    fi
    ;;
  3)
    xset -dpms
    xset s off
    xautolock -disable
    echo "🌷 DPMS disabled" 
    exit 0
    ;;
  4)
    ;;
  5)
    ;;
  *)
    ;;
esac

DPMS_DISABLED=$(xset q | grep "DPMS is Disabled" | awk '{ print $3}' )

if [ "$DPMS_DISABLED" == "Disabled" ]; then
  echo "🌷 off" 
  exit 33
else
  echo "🌷 on"
fi
