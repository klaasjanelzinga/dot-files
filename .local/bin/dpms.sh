#!/usr/bin/env bash

new_level=$1

case $new_level in
"start")
  # reset to defaults and start timers
  dpms.sh 
  xidlehook --socket ~/.local/xidlehook.socket \
		--timer 60  "dpms.sh 3" "dpms.sh" \
		--timer 240 "dpms.sh 1" "dpms.sh" \
		--timer 900 "dpms.sh 0" "dpms.sh"
  ;;
"stop")
  pkill xidlehook
  rm ~/.local/xidlehook.socket
  ;;
"enable")
  xidlehook-client --socket ../xidlehook.socket control --action enable
  ;;
"disable")
  xidlehook-client --socket ../xidlehook.socket control --action disable
  ;;
"query")
  xidlehook-client --socket ../xidlehook.socket query
  ;;
0)
  systemctl suspend
  ;;
1)
  blurlock
  ;;
2)
  notify-send "Locking..."
  ;;
3)
  xrandr --output HDMI2 --brightness .25
  brightnessctl -q s 15%
  wallpaper.sh stop
  ;;
*)
  xrandr --output HDMI2 --brightness 1
  brightnessctl -q s 60%
  nohup wallpaper.sh start </dev/null >~/.local/wallpaper-log 2>&1 &
  ;;
esac

