#!/bin/bash

echo "WARNING: For production use only, this will reset your code changes"
echo "Press any key to continue, or Ctrl+C to exit"
read userinput

while [ true ]; do
        git reset --hard HEAD
        git pull --rebase
        python bot.py
        if [ $?==0 ]; then
        	exit 0
        fi
done

