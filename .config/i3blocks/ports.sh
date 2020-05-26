#!/bin/bash

function check_port {
  curl -s $1 --head 2>&1 >/dev/null
  echo $?
}


result_string=""
for url in http://localhost:9000 http://localhost:9001 http://localhost:80/status http://localhost:8001/status http://localhost:1080  http://localhost:8123/health
do
  result=$(check_port ${url})
  if [ ${result} == 0 ]
    then
    result_string="👍 $result_string"
  else
    result_string="🔻 $result_string"
  fi
done
  

echo $result_string

