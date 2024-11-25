#!/bin/bash


# パッケージのインストール
sudo apt update
sudo apt install -y python3-pip

# ライブラリのインストール
pip3 install requests pandas discord.py

echo "Setup complete!"
