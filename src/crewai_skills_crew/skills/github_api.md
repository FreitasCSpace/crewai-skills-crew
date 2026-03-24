# Skill: github_api

## Purpose
Interact with the GitHub REST API using curl for repos, issues, PRs, releases, Actions, and org management.

## When to use
- Creating or managing repositories, branches, releases
- Listing, creating, updating, or closing issues and PRs
- Triggering or checking GitHub Actions workflows
- Managing teams, org members, or repo permissions
- When `gh` CLI is unavailable or you need finer API control

## Prerequisites
- `GITHUB_TOKEN` env var set (classic PAT or fine-grained token)
- Token needs appropriate scopes (repo, workflow, admin:org, etc.)

## How to execute

**List repos for a user/org:**
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/users/OWNER/repos?per_page=100&sort=updated" \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin):
    print(f'{r[\"full_name\"]:40s} ⭐{r[\"stargazers_count\"]:>5}  {r[\"language\"] or \"-\"}')"
```

**Create a repository:**
```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/user/repos" \
  -d '{"name":"my-repo","private":true,"description":"Created via API"}'
```

**Create an issue:**
```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/OWNER/REPO/issues" \
  -d '{"title":"Bug: something broke","body":"Details here","labels":["bug"]}'
```

**List open issues:**
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/issues?state=open&per_page=50" \
  | python3 -c "
import json,sys
for i in json.load(sys.stdin):
    if 'pull_request' not in i:
        print(f'#{i[\"number\"]:>4} {i[\"title\"]}')"
```

**Create a pull request:**
```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/OWNER/REPO/pulls" \
  -d '{"title":"feat: new feature","head":"feature-branch","base":"main","body":"Description"}'
```

**Merge a pull request:**
```bash
curl -s -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/OWNER/REPO/pulls/PR_NUMBER/merge" \
  -d '{"merge_method":"squash"}'
```

**Create a release:**
```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/OWNER/REPO/releases" \
  -d '{"tag_name":"v1.0.0","name":"Release 1.0.0","body":"Changelog here","draft":false}'
```

**List workflow runs (Actions):**
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs?per_page=10" \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin)['workflow_runs']:
    print(f'{r[\"id\"]} {r[\"status\"]:>12} {r[\"conclusion\"] or \"running\":>10} {r[\"name\"]}')"
```

**Trigger a workflow dispatch:**
```bash
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/OWNER/REPO/actions/workflows/WORKFLOW_ID/dispatches" \
  -d '{"ref":"main","inputs":{"param1":"value1"}}'
```

**Get file contents from a repo:**
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/contents/path/to/file.txt?ref=main" \
  | python3 -c "import json,sys,base64; print(base64.b64decode(json.load(sys.stdin)['content']).decode())"
```

**List branches:**
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/branches?per_page=100" \
  | python3 -c "import json,sys; [print(b['name']) for b in json.load(sys.stdin)]"
```

## Output contract
- stdout: JSON response from GitHub API
- HTTP 200/201: success
- HTTP 401: bad token / insufficient permissions
- HTTP 404: resource not found or no access
- HTTP 422: validation error (bad payload)

## Evaluate output
Always check HTTP status. Parse JSON to confirm the operation succeeded.
If 401: verify GITHUB_TOKEN is set and has the right scopes.
If 422: read the error message — usually a missing or invalid field.
