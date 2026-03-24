# Skill: git_ops

## Purpose
Perform Git and GitHub operations using the git and gh CLIs.

## When to use
- Cloning, committing, pushing, pulling repositories
- Reading repo status, logs, diffs
- Listing, creating, or reviewing GitHub PRs and issues
- Checking branch state or file history

## Prerequisites
- `git` installed and configured (name + email)
- `gh` installed and authenticated for GitHub operations

**Check both are ready:**
```bash
git --version && gh --version && gh auth status
```

## How to execute

**Clone a repo:**
```bash
git clone https://github.com/owner/repo.git
cd repo && git log --oneline -5
```

**Check repo status:**
```bash
git status
git log --oneline -10
git diff --stat
```

**Stage and commit:**
```bash
git add -A
git commit -m "feat: describe what changed"
```

**Push:**
```bash
git push origin main
```

**List open PRs:**
```bash
gh pr list --repo owner/repo --state open \
  --json number,title,author,state \
  --jq '.[] | "\(.number) | \(.title) | \(.author.login)"'
```

**View a specific PR:**
```bash
gh pr view 42 --repo owner/repo
```

**List open issues:**
```bash
gh issue list --repo owner/repo --state open \
  --json number,title \
  --jq '.[] | "\(.number): \(.title)"'
```

**Create a branch:**
```bash
git checkout -b feature/my-branch
```

## Output contract
- stdout: command output
- exit_code 0: success
- exit_code 1+: auth error, repo not found, network issue

## Evaluate output
If `gh auth status` fails: user needs to run `gh auth login` first.
Always confirm current branch before committing.
If clone fails with 403: check repo visibility and token permissions.
