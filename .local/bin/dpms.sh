#!/usr/bin/env bash

new_level=$1
socket_file=~/.local/xidlehook.socket

case $new_level in
"help" | "--help")
	echo "dpms.sh arg"
	echo " arg:"
	echo "	restart"
	echo "	start"
	echo "	stop"
	echo "	enable"
	echo "	disable"
	echo "	query"
	echo "	help - this"
	echo "	0 - suspend"
	echo "	1 - lock"
	echo "	3 - inactive"
	echo "no arg is normalize"
  ;;
"restart")
	i3-msg 'exec dpms.sh stop'
	sleep 1
	i3-msg 'exec dpms.sh start'
	;;
"start")
  # reset to defaults and start timers
  dpms.sh 
  xidlehook --socket ${socket_file} \
		--timer 120 "dpms.sh 3" "dpms.sh" \
		--timer 360 "dpms.sh 1" "dpms.sh" \
		--timer 900 "dpms.sh 0" "dpms.sh"
  ;;
"stop")
  pkill xidlehook
  rm ${socket_file}
  ;;
"enable")
  xidlehook-client --socket ${socket_file} control --action enable
  ;;
"disable")
  xidlehook-client --socket ${socket_file} control --action disable
  ;;
"query")
  xidlehook-client --socket ${socket_file}  query
  ;;
0)
  systemctl suspend
  ;;
1)
	ps aux | grep i3lock | grep -v grep >/dev/null
	[ $? != 0 ] && blurlock
  ;;
2)
	# Do not use notify, since it will trigger some x-events causing xidle to restart.
  ;;
3)
  xrandr --output HDMI2 --brightness .20
  brightnessctl -q s 10%
  wallpaper.sh stop
  ;;
*)
  xrandr --output HDMI2 --brightness 1
  brightnessctl -q s 50%
  nohup wallpaper.sh start </dev/null >~/.local/wallpaper-log 2>&1 &
  ;;
esac

