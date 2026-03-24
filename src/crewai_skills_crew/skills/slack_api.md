# Skill: slack_api

## Purpose
Send messages, manage channels, and interact with Slack workspaces via the Slack Web API.

## When to use
- Sending notifications or reports to Slack channels
- Listing channels, users, or messages
- Creating channels or managing channel membership
- Uploading files to Slack
- Building automated Slack workflows

## Prerequisites
- `SLACK_BOT_TOKEN` env var (starts with `xoxb-`) — Bot User OAuth Token from Slack App settings
- Bot must be invited to the target channel
- Required scopes: `chat:write`, `channels:read`, `channels:manage`, `files:write`, `users:read`

## How to execute

**Send a message:**
```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0123456789",
    "text": "Hello from the crew! :robot_face:",
    "mrkdwn": true
  }' | python3 -c "import json,sys; r=json.load(sys.stdin); print('OK' if r['ok'] else f'ERROR: {r[\"error\"]}')"
```

**Send a rich message (blocks):**
```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C0123456789",
    "blocks": [
      {"type": "header", "text": {"type": "plain_text", "text": "Task Report"}},
      {"type": "section", "text": {"type": "mrkdwn", "text": "*Status:* Complete\n*Files:* 3 generated\n*Duration:* 2m 15s"}},
      {"type": "divider"},
      {"type": "section", "text": {"type": "mrkdwn", "text": "See full report in the output artifacts."}}
    ]
  }'
```

**List channels:**
```bash
curl -s "https://slack.com/api/conversations.list" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "types=public_channel,private_channel&limit=100" \
  | python3 -c "
import json,sys
for c in json.load(sys.stdin).get('channels',[]):
    print(f'{c[\"id\"]:>12} #{c[\"name\"]}')"
```

**Find channel by name:**
```bash
curl -s "https://slack.com/api/conversations.list" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "types=public_channel&limit=200" \
  | python3 -c "
import json,sys
target = 'general'
for c in json.load(sys.stdin).get('channels',[]):
    if c['name'] == target:
        print(f'Channel ID: {c[\"id\"]}')
        break
else:
    print('NOT FOUND')"
```

**Upload a file:**
```bash
curl -s -X POST "https://slack.com/api/files.uploadV2" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -F file=@./output/report.md \
  -F channel_id=C0123456789 \
  -F initial_comment="Here's the report" \
  -F title="Report"
```

**List users:**
```bash
curl -s "https://slack.com/api/users.list" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  | python3 -c "
import json,sys
for u in json.load(sys.stdin).get('members',[]):
    if not u.get('is_bot') and not u.get('deleted'):
        print(f'{u[\"id\"]:>12} {u[\"real_name\"]}')"
```

**Create a channel:**
```bash
curl -s -X POST "https://slack.com/api/conversations.create" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "project-updates", "is_private": false}'
```

**Get recent messages from a channel:**
```bash
curl -s "https://slack.com/api/conversations.history" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "channel=C0123456789&limit=10" \
  | python3 -c "
import json,sys
for m in json.load(sys.stdin).get('messages',[]):
    print(f'{m.get(\"user\",\"bot\"):>12}: {m[\"text\"][:100]}')"
```

## Output contract
- stdout: JSON response with `ok: true/false`
- `ok: true` = success
- `ok: false` + `error` field = something went wrong

## Common errors
- `not_in_channel`: bot needs to be invited to the channel first
- `channel_not_found`: wrong channel ID
- `invalid_auth`: bad token
- `missing_scope`: token needs additional OAuth scopes

## Evaluate output
Always check `ok` field in response. If false, read the `error` field.
If `not_in_channel`: invite the bot with `/invite @botname` in Slack.
