set +x
file=$(find ~/pCloudDrive/klaasjan/pics/desktop/*.png |sort -R |tail -1)
swaymsg output "*"  bg $file fill
