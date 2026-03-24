# Skill: jira_api

## Purpose
Manage Jira projects, issues, sprints, and boards via the Jira Cloud REST API.

## When to use
- Creating, updating, or transitioning Jira issues
- Listing issues by project, sprint, assignee, or JQL query
- Managing sprints, boards, and epics
- Adding comments, attachments, or worklogs
- Generating reports from Jira data

## Prerequisites
- `JIRA_BASE_URL` env var (e.g., `https://yourcompany.atlassian.net`)
- `JIRA_EMAIL` env var (your Atlassian account email)
- `JIRA_API_TOKEN` env var (API token from https://id.atlassian.com/manage-profile/security/api-tokens)

## How to execute

**Search issues with JQL:**
```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search" \
  -H "Content-Type: application/json" \
  -d '{"jql": "project = PROJ AND status != Done ORDER BY created DESC", "maxResults": 20, "fields": ["summary","status","assignee","priority"]}' \
  | python3 -c "
import json,sys
data = json.load(sys.stdin)
for i in data['issues']:
    f = i['fields']
    assignee = f['assignee']['displayName'] if f.get('assignee') else 'Unassigned'
    print(f'{i[\"key\"]:>10} [{f[\"status\"][\"name\"]:>12}] {f[\"summary\"]}  ({assignee})')"
```

**Get issue details:**
```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issue/PROJ-123" \
  | python3 -m json.tool
```

**Create an issue:**
```bash
curl -s -X POST -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issue" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "Implement new feature",
      "description": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Details here"}]}]},
      "issuetype": {"name": "Task"},
      "priority": {"name": "Medium"},
      "assignee": {"accountId": "ACCOUNT_ID"}
    }
  }'
```

**Update an issue:**
```bash
curl -s -X PUT -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issue/PROJ-123" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"summary": "Updated title", "priority": {"name": "High"}}}'
```

**Transition an issue (change status):**
```bash
# First get available transitions
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issue/PROJ-123/transitions" \
  | python3 -c "import json,sys; [print(f'{t[\"id\"]:>4} {t[\"name\"]}') for t in json.load(sys.stdin)['transitions']]"

# Then apply a transition
curl -s -X POST -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issue/PROJ-123/transitions" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "31"}}'
```

**Add a comment:**
```bash
curl -s -X POST -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/issue/PROJ-123/comment" \
  -H "Content-Type: application/json" \
  -d '{"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Work completed."}]}]}}'
```

**List projects:**
```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/project" \
  | python3 -c "import json,sys; [print(f'{p[\"key\"]:>8} {p[\"name\"]}') for p in json.load(sys.stdin)]"
```

**Get sprint issues (Agile API):**
```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/agile/1.0/board/BOARD_ID/sprint?state=active" \
  | python3 -c "
import json,sys
for s in json.load(sys.stdin)['values']:
    print(f'Sprint: {s[\"name\"]} (ID: {s[\"id\"]}, State: {s[\"state\"]})')"
```

**My open issues:**
```bash
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/search" \
  -H "Content-Type: application/json" \
  -d '{"jql": "assignee = currentUser() AND status != Done", "maxResults": 50, "fields": ["summary","status","priority"]}' \
  | python3 -c "
import json,sys
for i in json.load(sys.stdin)['issues']:
    f = i['fields']
    print(f'{i[\"key\"]:>10} [{f[\"status\"][\"name\"]:>12}] {f[\"summary\"]}')"
```

## Output contract
- stdout: JSON response
- HTTP 200/201: success
- HTTP 401: invalid credentials
- HTTP 404: issue/project not found
- HTTP 400: bad request (invalid fields or JQL)

## Evaluate output
If 401: verify JIRA_EMAIL and JIRA_API_TOKEN are set.
If 400 on create: check field names — they vary by project configuration.
Always get transitions list before trying to transition an issue.
