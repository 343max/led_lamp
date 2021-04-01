#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

sudo killall python3
sudo python3 -u $DIR/server.py </dev/null &>>/tmp/server_log &
