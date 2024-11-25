#!/bin/bash

git clone https://github.com/rintaro-s/timetable.git
cd timetable

# パッケージのインストール
sudo apt update
sudo apt install -y python3-pip

# ライブラリのインストール
pip3 install requests pandas discord.py

echo "Setup complete!"
