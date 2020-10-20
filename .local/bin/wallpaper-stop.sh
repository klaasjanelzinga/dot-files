#!/usr/bin/env bash

kill $(ps aux | grep wallpaper-start.sh | grep -v grep | awk '{ print $2 }')

