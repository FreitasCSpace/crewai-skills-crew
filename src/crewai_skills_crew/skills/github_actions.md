# Skill: github_actions

## Purpose
Create and manage CI/CD pipelines using GitHub Actions workflows.

## When to use
- Setting up automated testing, building, or deployment
- Creating workflow YAML files for GitHub repositories
- Debugging failing workflows
- Implementing CI/CD for any language or platform

## How to execute

**Create a basic CI workflow:**
```bash
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest

      - name: Run tests
        run: pytest -v
EOF
```

**Node.js CI workflow:**
```bash
cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]

    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: npm

      - run: npm ci
      - run: npm run build
      - run: npm test
EOF
```

**Docker build and push workflow:**
```bash
cat > .github/workflows/docker.yml << 'EOF'
name: Docker Build & Push

on:
  push:
    tags: ['v*']

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/myapp:latest
            ${{ secrets.DOCKER_USERNAME }}/myapp:${{ github.ref_name }}
EOF
```

**Deploy to Vercel workflow:**
```bash
cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: --prod
EOF
```

**Scheduled workflow (cron):**
```bash
cat > .github/workflows/scheduled.yml << 'EOF'
name: Daily Report

on:
  schedule:
    - cron: '0 9 * * 1-5'  # 9 AM UTC, Mon-Fri
  workflow_dispatch:         # Allow manual trigger

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate report
        run: python3 generate_report.py
        env:
          API_KEY: ${{ secrets.API_KEY }}
EOF
```

**Workflow with services (database):**
```bash
cat > .github/workflows/test-with-db.yml << 'EOF'
name: Test with DB

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest -v
        env:
          DATABASE_URL: postgres://test:test@localhost:5432/testdb
EOF
```

**Release workflow (auto-create release on tag):**
```bash
cat > .github/workflows/release.yml << 'EOF'
name: Release

on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          generate_release_notes: true
EOF
```

**Check workflow runs via CLI:**
```bash
gh run list --limit 10
gh run view RUN_ID
gh run view RUN_ID --log
```

## Output contract
- Workflow files are YAML in `.github/workflows/`
- Workflows trigger automatically based on the `on:` configuration
- Check status via GitHub UI or `gh run list`

## Evaluate output
If workflow fails: check logs with `gh run view RUN_ID --log`.
Common issues: missing secrets, wrong file paths, version mismatches.
Always test locally first before relying on CI.
Use `workflow_dispatch` trigger for manual testing during development.
