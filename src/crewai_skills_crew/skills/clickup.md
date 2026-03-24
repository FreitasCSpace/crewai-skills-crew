# Skill: clickup

## Purpose
Manage ClickUp workspaces, spaces, lists, tasks, and comments via the ClickUp API v2.

## When to use
- Creating, updating, or listing tasks in ClickUp
- Managing lists, folders, and spaces
- Adding comments, attachments, or custom field values
- Querying task status, assignees, or due dates
- Automating project management workflows

## Prerequisites
- `CLICKUP_API_TOKEN` env var (Personal API Token from ClickUp Settings → Apps)
- Know your Team ID (workspace ID) — get it from the first call below

## How to execute

**Get workspaces (teams):**
```bash
curl -s -H "Authorization: $CLICKUP_API_TOKEN" \
  "https://api.clickup.com/api/v2/team" \
  | python3 -c "
import json,sys
data = json.load(sys.stdin)
for t in data['teams']:
    print(f'Team: {t[\"name\"]} (ID: {t[\"id\"]})')
    for m in t.get('members',[])[:5]:
        print(f'  - {m[\"user\"][\"username\"]}')"
```

**List spaces in a workspace:**
```bash
curl -s -H "Authorization: $CLICKUP_API_TOKEN" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/space?archived=false" \
  | python3 -c "
import json,sys
for s in json.load(sys.stdin)['spaces']:
    print(f'{s[\"id\"]:>12} {s[\"name\"]}')"
```

**List folders in a space:**
```bash
curl -s -H "Authorization: $CLICKUP_API_TOKEN" \
  "https://api.clickup.com/api/v2/space/SPACE_ID/folder?archived=false" \
  | python3 -c "
import json,sys
for f in json.load(sys.stdin)['folders']:
    print(f'{f[\"id\"]:>12} {f[\"name\"]}')
    for l in f.get('lists',[]):
        print(f'  List: {l[\"id\"]:>12} {l[\"name\"]}')"
```

**List tasks in a list:**
```bash
curl -s -H "Authorization: $CLICKUP_API_TOKEN" \
  "https://api.clickup.com/api/v2/list/LIST_ID/task?archived=false&include_closed=false" \
  | python3 -c "
import json,sys
for t in json.load(sys.stdin)['tasks']:
    assignees = ', '.join(a['username'] for a in t.get('assignees',[]))
    print(f'{t[\"id\"]:>12} [{t[\"status\"][\"status\"]:>12}] {t[\"name\"]}  ({assignees})')"
```

**Create a task:**
```bash
curl -s -X POST -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.clickup.com/api/v2/list/LIST_ID/task" \
  -d '{
    "name": "Task title here",
    "description": "Task description in markdown",
    "status": "to do",
    "priority": 2,
    "due_date": 1700000000000,
    "assignees": [USER_ID],
    "tags": ["backend", "urgent"]
  }'
```

**Update a task:**
```bash
curl -s -X PUT -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.clickup.com/api/v2/task/TASK_ID" \
  -d '{"status": "in progress", "priority": 1}'
```

**Add a comment to a task:**
```bash
curl -s -X POST -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.clickup.com/api/v2/task/TASK_ID/comment" \
  -d '{"comment_text": "Update: this is done."}'
```

**Get task details:**
```bash
curl -s -H "Authorization: $CLICKUP_API_TOKEN" \
  "https://api.clickup.com/api/v2/task/TASK_ID" \
  | python3 -m json.tool
```

**Search tasks by name:**
```bash
curl -s -H "Authorization: $CLICKUP_API_TOKEN" \
  "https://api.clickup.com/api/v2/team/TEAM_ID/task?name=search%20term&include_closed=false" \
  | python3 -c "
import json,sys
for t in json.load(sys.stdin).get('tasks',[]):
    print(f'{t[\"id\"]} {t[\"name\"]} [{t[\"status\"][\"status\"]}]')"
```

**Create a list:**
```bash
curl -s -X POST -H "Authorization: $CLICKUP_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.clickup.com/api/v2/folder/FOLDER_ID/list" \
  -d '{"name": "Sprint 42", "content": "Sprint tasks"}'
```

## Priority values
- 1 = Urgent, 2 = High, 3 = Normal, 4 = Low

## Output contract
- stdout: JSON response
- HTTP 200: success
- HTTP 401: invalid token
- HTTP 404: resource not found
- HTTP 429: rate limited — wait and retry

## Evaluate output
Always verify the task was created/updated by checking the response JSON.
If 401: check CLICKUP_API_TOKEN is set correctly.
If empty task list: verify the LIST_ID is correct; try listing spaces first.
