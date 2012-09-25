#!/bin/bash

echo "========== WARNING =========: For production use only, this will reset your uncommited code changes"
echo "Press any key to continue, or Ctrl+C to exit"
read userinput

while [ true ]; do
        python main.py
        if [ $? -eq 0 ]; then
                exit 0
        fi
        git reset --hard HEAD
        git pull --rebase
done
