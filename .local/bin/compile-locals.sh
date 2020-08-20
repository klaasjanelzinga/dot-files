#!/usr/bin/env bash

set -e

echo "Compiling i3"
i3_dir=~/projects/i3


if [ -d $i3_dir ]
then
  cd $i3_dir
  git status
  git pull
  autoreconf -fi
  rm -rf build && mkdir -p build && cd build
  ../configure
  make -j8
  i3 --moreversion
  echo "Install (will sudo)?"
  read -s -n 1 key
  sudo make install 
fi
