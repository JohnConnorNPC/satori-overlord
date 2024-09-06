#!/bin/bash

# Change to the /minion directory
cd /minion

# Remove the old minion.py file
rm minion.py

# Download the new minion.py file from the server
wget -P /minion/ ##server_url##/files/minion.py

# Convert the file to Unix format
dos2unix /minion/minion.py

pkill -f "python3 /minion/minion.py"
