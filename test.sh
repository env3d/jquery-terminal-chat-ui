curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{ "model": "Qwen2-0.5B-Instruct", "messages": [{"role": "user", "content": "Hello, can you tell me a joke for me?"}], "temperature": 0.5 }'