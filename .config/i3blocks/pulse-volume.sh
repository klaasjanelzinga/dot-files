#!/usr/bin/env bash

# Speaker unicode: 🔈
# Speaker muted: 🔇
# Speaker loud: 🔊
# Speaker mid: 🔉
# Microphone: 🎤
# Music: 🎵
# 

set -e 

contains() {
    string="$1"
    substring="$2"
    if test "${string#*$substring}" != "$string"
    then
        return 0    # $substring is in $string
    else
        return 1    # $substring is not in $string
    fi
}

control=$scontrol

case $BLOCK_BUTTON in
2)
  amixer -q sset $control toggle
  ;;
1 | 4)
  amixer -q sset $control 5%+
  ;;
3 | 5)
  amixer -q sset $control 5%-
  ;;
esac

control_status=$(amixer sget $control | tail -1)
control_on_off=$(echo $control_status | cut -d\: -f2 | awk '{print $5}')
control_type=$(echo $control_status | cut -d\: -f2 | awk '{print $1}')
control_level=$(echo $control_status | cut -d\: -f2 | awk '{print $2}')
control_percentage=$(echo $control_status | cut -d\: -f2 | awk '{print $3}' | tr -d '\[\]' )
control_db=$(echo $control_status | cut -d\: -f2 | awk '{print $4}')
control_muted="NO"
contains $control_on_off "off" && control_muted="YES"

if [ $control_muted == "YES" ]; then
  echo "$LABEL $MUTED_LABEL"
  exit 0
fi

echo "$LABEL $control_percentage"
exit 0

