set +x
file=$(find ~/pCloudDrive/klaasjan/pics/desktop/*.png |sort -R |tail -1)
export DISPLAY=:0
feh --bg-scale $file
# export I3SOCK=$(ls /run/user/1000/sway-ipc.1000.*.sock)
# swaymsg output "*"  bg $file fill
