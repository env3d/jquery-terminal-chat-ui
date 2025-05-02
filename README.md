# jquery-terminal-chat-ui
Basic chat ui using jquery-terminal

# Backend setup

Using fastchat https://github.com/lm-sys/FastChat as backend model server

```bash
pip3 install "fschat[model_worker,webui] fastapi httpx"
# python -m fastchat.serve.cli --model-path Qwen/Qwen2-0.5B-Instruct --device cpu

python3 -m fastchat.serve.controller &
python3 -m fastchat.serve.model_worker --model-path Qwen/Qwen2-0.5B-Instruct --device cpu &
python3 -m fastchat.serve.openai_api_server --port 8080 &

uvicorn app:app --host 0.0.0.0 --port 8000
```
