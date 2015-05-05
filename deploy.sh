#!/bin/sh

ps -ef | grep app.py | grep -v -E 'grep'| awk '{print $2}' | xargs kill -9
python app.py 9001 & 
