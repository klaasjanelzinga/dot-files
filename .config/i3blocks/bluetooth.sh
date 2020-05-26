#!/bin/bash

case $BLOCK_BUTTON in
  1)
    i3-msg exec blueman-manager
    ;;
esac


statusLine=$(bluetoothctl devices | wc -l)

echo "🦷 $statusLine"

