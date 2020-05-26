#!/bin/bash

root_disk=$(df -h / | tail -1)
available=$(echo $root_disk | awk '{ print $4 }') 
used=$(echo $root_disk | awk '{ print $3 }') 
size=$(echo $root_disk | awk '{ print $2 }') 
percentage_used=$(echo $root_disk | awk '{ print $5 }') 

case $BLOCK_BUTTON in
  2|  1 | 4 | 3 | 5)
    echo $root_disk
    exit 0
    ;;
  *)
    ;;
esac

red='"red"'
white='"white"'

percentage=$(echo $percentage_used | tr % ' ')
if [ $percentage -gt 70 ]
then
    echo "<span foreground=$white><b>/ $available ($percentage_used)</b></span>"
    exit 33
elif [ $percentage -gt 50 ]
then
    echo "<span foreground=$red>/ $available ($percentage_used)</span>"
else
    echo "/ $available ($percentage_used)"
fi

exit 0
