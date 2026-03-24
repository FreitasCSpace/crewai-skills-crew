# Skill: http_request

## Purpose
Make HTTP requests to any REST API or URL using curl. No SDK required.

## When to use
- Fetching data from a public or authenticated REST API
- Posting data to a service or webhook
- Downloading files from URLs
- Checking if a service is alive

## How to execute

**GET request (JSON API):**
```bash
curl -s "https://api.example.com/endpoint" \
  -H "Accept: application/json" | python3 -m json.tool
```

**GET with auth:**
```bash
curl -s "https://api.example.com/data" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Accept: application/json"
```

**POST with JSON body:**
```bash
curl -s -X POST "https://api.example.com/endpoint" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{"key": "value", "other": 123}'
```

**Save response to file:**
```bash
curl -s "https://api.example.com/data" -o data.json
echo "Saved. Size: $(wc -c < data.json) bytes"
```

**Check HTTP status code:**
```bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.example.com/health")
echo "HTTP Status: $STATUS"
[ "$STATUS" = "200" ] && echo "OK" || echo "FAILED: $STATUS"
```

**Download a file:**
```bash
curl -sL "https://example.com/file.csv" -o downloaded.csv
wc -l downloaded.csv
```

## Auth patterns
- Bearer token: `-H "Authorization: Bearer $TOKEN"`
- API key header: `-H "X-API-Key: $API_KEY"`
- Basic auth: `-u "$USER:$PASS"`
- Always read credentials from environment variables — never hardcode secrets

## Output contract
- stdout: response body
- exit_code 0: curl succeeded — but also check HTTP status (curl exits 0 even on 404/500)
- exit_code 6: DNS failure (host not found)
- exit_code 7: connection refused
- exit_code 28: request timed out

## Evaluate output
- Parse the response — is it valid? Is it the data you expected?
- HTTP 4xx = auth or bad request. HTTP 5xx = server error.
- If the response is large, save to file first then inspect with head/python
- Always verify the data before passing it to the next step
