#!/bin/bash
cd /minion
while true; do
    python3 /minion/minion.py
    if [ $? -ne 0 ]; then
        echo "minion.py crashed with exit code $?.  Respawning..." >&2
        sleep 1
    else
        break
    fi
done
