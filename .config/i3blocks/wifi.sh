#!/bin/bash

connectivity=$(nmcli n connectivity)

white='"white"'

if [ "$connectivity" != "full" ]
then
  echo "<span foreground=$white><b>📡 DOWN</b></span>"
  exit 33
fi

# - fetch connectivity info 
wifi_device=$(nmcli c show --active | grep wifi | awk '{ print $4 }')

# - fetch device info
ip_address=$(nmcli device show $wifi_device | grep IP4.ADDRESS | awk '{ print $2 }')
dns_address=$(nmcli device show $wifi_device | grep IP4.DNS | head -1 | awk '{ print $2 }')
gateway_address=$(nmcli device show $wifi_device | grep IP4.GATEWAY | awk '{ print $2 }')

# - fetch scan_results
scan_results=$(nmcli dev wifi list --rescan no | grep  -e '^*' | sed 's/\*/_/')
signal_strength=$(echo $scan_results | awk ' { print $8 }')
ssid=$(echo $scan_results | awk ' { print $3 }')

default_msg="$ssid $signal_strength%"
long_msg="$ip_address @ $wifi_device" 
alt_msg="DNS: $dns_address GW: $gateway_address"
connectivity_msg="connectivity $connectivity"

msg=$default_msg

# Left click
if [[ "${BLOCK_BUTTON}" -eq 3 ]]; then
  msg=$long_msg
# Middle click
elif [[ "${BLOCK_BUTTON}" -eq 2 ]]; then
  msg=$connectivity_msg
# Right click
elif [[ "${BLOCK_BUTTON}" -eq 1 ]]; then
  msg=$alt_msg
fi

echo "📡 $msg"

