#!/usr/bin/env bash

if [ -z $1 ]; then
  echo "get-password.sh [ssh|a2bc|discover|gitlab-oauth|portal]"
  exit 1
fi

set -e
SESSION_KEY=$(bw unlock --raw)
bw sync --session $SESSION_KEY

case $1 in
  "ssh")
    bw get password "ssh private key thinkpad" --session $SESSION_KEY | xclip -selection c
    ;;
  "a2bc")
    bw get password portal.a2bc.com --session $SESSION_KEY | xclip -selection c
    ;;
  "discover")
    bw get password discover.movingspirits.nl --session $SESSION_KEY | xclip -selection c
    ;;
  "gitlab-oauth")
    bw get password "gitlab oauth springtimegroup" --session $SESSION_KEY | xclip -selection c
    ;;
  "portal")
    bw get password portal.movingspirits.nl --session $SESSION_KEY | xclip -selection c
    ;;
  *)
    echo "Unknown password"
    exit 1
esac

echo "Password is in the clipboard"
exit 0
