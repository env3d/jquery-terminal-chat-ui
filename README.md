# jquery-terminal-chat-ui
Basic chat ui using jquery-terminal

# Backend setup

## Manually installing llama.cpp 
```bash

# Make sure build tools are available in OS
sudo apt update
sudo apt install -y build-essential cmake git
sudo apt install nginx

# install llama.cpp
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp

cmake -B build
cmake --build build --config Release


cd ..
wget https://huggingface.co/NousResearch/DeepHermes-3-Llama-3-3B-Preview-GGUF/resolve/main/DeepHermes-3-Llama-3-3B-Preview-q4.gguf

./llama.cpp/build/bin/llama-server -m DeepHermes-3-Llama-3-3B-Preview-q4.gguf &

sudo rm /etc/nginx/sites-enabled/default
sudo ln -fs $(pwd)/nginx-default /etc/nginx/sites-enabled/default
sudo service nginx start

```

## Use llama-cpp-python

```bash

# For dev
pip install 'llama-cpp-python[server]'

wget https://huggingface.co/NousResearch/DeepHermes-3-Llama-3-3B-Preview-GGUF/resolve/main/DeepHermes-3-Llama-3-3B-Preview-q4.gguf

python3 -m llama_cpp.server --host 0.0.0.0 --port 8080 --model ./DeepHermes-3-Llama-3-3B-Preview-q4.gguf 

# Run image generator
uvicorn image_gen:app

```


```bash
# For production

# Make sure build tools are available in OS
sudo apt update
sudo apt install nginx
sudo ln -fs $(pwd)/nginx-default /etc/nginx/sites-enabled/default
chmod 755 /home/ubuntu
sed -i 's/workspaces/home\/ubuntu/' nginx-default
sudo service nginx start

python -m venv .env
source .env/bin/activate
pip install torch diffusers transformers accelerate protobuf sentencepiece fastapi uvicorn

CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install 'llama-cpp-python[server]'
wget -P /opt/dlami/nvme https://huggingface.co/NousResearch/DeepHermes-3-Mistral-24B-Preview-GGUF/resolve/main/DeepHermes-3-Mistral-24B-Preview-q4.gguf
python3 -m llama_cpp.server --host 0.0.0.0 --port 8080 --model /opt/dlami/nvme/DeepHermes-3-Mistral-24B-Preview-q4.gguf --n_gpu_layers 41

export HF_TOKEN=YOUR HF TOKEN
export HF_HOME=/opt/dlami/nvme/hf

# Run image generator
PROD=true uvicorn image_gen:app
```

# Old Backend Setup

Using fastchat https://github.com/lm-sys/FastChat as backend model server

```bash
pip3 install "fschat[model_worker,webui] fastapi httpx"
# python -m fastchat.serve.cli --model-path Qwen/Qwen2-0.5B-Instruct --device cpu

python3 -m fastchat.serve.controller &
python3 -m fastchat.serve.model_worker --model-path Qwen/Qwen2-0.5B-Instruct --device cpu &
python3 -m fastchat.serve.openai_api_server --port 8080 &

uvicorn app:app --host 0.0.0.0 --port 8000
```
