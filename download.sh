#!/bin/bash

# Clone the repository
git clone https://github.com/rintaro-s/timetable.git
cd timetable

# Update and install necessary packages
sudo apt update
sudo apt install -y python3-pip

# Install Python packages
pip3 install requests pandas discord.py

echo "Setup complete!"
