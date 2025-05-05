curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -N \
  -d '{
    "model": "llama",
    "messages": [{"role": "user", "content": "Tell me a joke."}],
    "stream": true
  }'
