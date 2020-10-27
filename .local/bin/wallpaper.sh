#!/usr/bin/env bash

new_level=$1

case $new_level in
"start")
	while [ 0 ]; do
  	file=$(find ~/pCloudDrive/klaasjan/pics/desktop/*.png |sort -R |tail -1)
  	feh -q --bg-scale $file
  	sleep 360
	done
  ;;
"stop")
	pid=$(ps aux | grep "wallpaper.sh start" | grep -v grep | awk '{ print $2 }')
	[ "$pid" != "" ] && kill $pid
	;;
*)
	echo "Unknown option $new_level. Use $0 start|stop"
	;;
esac

# export I3SOCK=$(ls /run/user/1000/sway-ipc.1000.*.sock)
# swaymsg output "*"  bg $file fill
