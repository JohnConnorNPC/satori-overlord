#!/bin/bash
cd /overlord
chmod +x Overlord
while true; do
    ./Overlord
    if [ $? -ne 0 ]; then
        echo "Overlord crashed with exit code $?.  Respawning..." >&2
        sleep 5
    else
        break
    fi
done
