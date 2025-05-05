#!/bin/bash

# Make sure build tools are available in OS
sudo apt update
sudo apt install -y build-essential cmake git
sudo apt install -y nginx
sudo ln -sf $(pwd)/nginx-default /etc/nginx/sites-enabled/default
sudo service nginx start

# llama.cpp
pip install 'llama-cpp-python[server]'

# Download model
wget https://huggingface.co/NousResearch/DeepHermes-3-Llama-3-3B-Preview-GGUF/resolve/main/DeepHermes-3-Llama-3-3B-Preview-q4.gguf

# Serve model
python3 -m llama_cpp.server --host 0.0.0.0 --port 8080 --model ./DeepHermes-3-Llama-3-3B-Preview-q4.gguf 