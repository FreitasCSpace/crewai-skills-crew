# Skill: openai_api

## Purpose
Call OpenAI APIs (Chat Completions, Embeddings, Images, Audio, Assistants) using curl or Python.

## When to use
- Generating text completions (GPT-4o, GPT-4, GPT-3.5)
- Creating embeddings for semantic search
- Generating or editing images (DALL-E)
- Transcribing audio (Whisper)
- When you need an LLM sub-call within a larger task

## Prerequisites
- `OPENAI_API_KEY` env var set

## How to execute

**Chat completion (curl):**
```bash
curl -s "https://api.openai.com/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Summarize the key benefits of microservices architecture in 3 bullet points."}
    ],
    "temperature": 0.7,
    "max_tokens": 500
  }' | python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'])"
```

**Chat completion (Python — better for complex prompts):**
```bash
pip install openai --quiet && python3 -c "
from openai import OpenAI
import os

client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Write a haiku about coding.'}
    ],
    temperature=0.7
)
print(response.choices[0].message.content)
"
```

**Process a file with GPT:**
```bash
python3 -c "
from openai import OpenAI
import json

client = OpenAI()

with open('data.json') as f:
    data = json.load(f)

response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {'role': 'system', 'content': 'Analyze the following data and provide insights.'},
        {'role': 'user', 'content': json.dumps(data[:10])}  # Send first 10 records
    ]
)
print(response.choices[0].message.content)
"
```

**Generate embeddings:**
```bash
curl -s "https://api.openai.com/v1/embeddings" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-3-small", "input": "Your text here"}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Dimensions: {len(d[\"data\"][0][\"embedding\"])}')"
```

**Generate an image (DALL-E):**
```bash
curl -s "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "dall-e-3", "prompt": "A futuristic city at sunset", "n": 1, "size": "1024x1024"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data'][0]['url'])"
```

**Transcribe audio (Whisper):**
```bash
curl -s "https://api.openai.com/v1/audio/transcriptions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file=@audio.mp3 \
  -F model=whisper-1 \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['text'])"
```

**Structured output (JSON mode):**
```bash
python3 -c "
from openai import OpenAI
import json

client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o',
    response_format={'type': 'json_object'},
    messages=[
        {'role': 'system', 'content': 'Respond in JSON format.'},
        {'role': 'user', 'content': 'List 3 programming languages with their year of creation and creator.'}
    ]
)
data = json.loads(response.choices[0].message.content)
print(json.dumps(data, indent=2))
"
```

**List available models:**
```bash
curl -s "https://api.openai.com/v1/models" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  | python3 -c "import json,sys; [print(m['id']) for m in sorted(json.load(sys.stdin)['data'], key=lambda x: x['id']) if 'gpt' in m['id']]"
```

## Output contract
- stdout: API response (text, JSON, or URL)
- HTTP 200: success
- HTTP 401: invalid API key
- HTTP 429: rate limited — wait and retry
- HTTP 400: bad request (invalid model, too many tokens, etc.)

## Evaluate output
If 401: check OPENAI_API_KEY is set and valid.
If 429: implement exponential backoff or reduce request rate.
If response is truncated: increase max_tokens.
Always validate structured output before using it downstream.
