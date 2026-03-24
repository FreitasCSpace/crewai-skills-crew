# Skill: vercel

## Purpose
Deploy web applications to Vercel — frontend apps, serverless functions, and full-stack Next.js projects.

## When to use
- Deploying React, Next.js, Vue, or static sites
- Creating serverless API routes
- Managing environment variables and domains
- Checking deployment status and logs
- Preview deployments for branches/PRs

## Prerequisites
- Vercel CLI: `npm i -g vercel`
- Logged in: `vercel login` or `VERCEL_TOKEN` env var
- Verify: `vercel --version && vercel whoami`

## How to execute

**Deploy current directory:**
```bash
vercel --yes               # Preview deployment
vercel --prod --yes        # Production deployment
```

**Deploy with environment variables:**
```bash
vercel --env DATABASE_URL=postgres://... --yes
```

**List deployments:**
```bash
vercel ls --limit 10
```

**List projects:**
```bash
vercel project ls
```

**Set environment variables:**
```bash
# Add env var for all environments
echo "my-secret-value" | vercel env add SECRET_KEY production

# List env vars
vercel env ls
```

**Link to existing project:**
```bash
vercel link
```

**View deployment logs:**
```bash
vercel logs DEPLOYMENT_URL
```

**Remove a deployment:**
```bash
vercel rm DEPLOYMENT_URL --yes
```

**Create a serverless function (api/):**
```bash
mkdir -p api

cat > api/hello.ts << 'EOF'
import type { VercelRequest, VercelResponse } from '@vercel/node';

export default function handler(req: VercelRequest, res: VercelResponse) {
  const { name = 'World' } = req.query;
  res.status(200).json({ message: `Hello ${name}!` });
}
EOF
```

**Create vercel.json configuration:**
```bash
cat > vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    { "src": "api/**/*.ts", "use": "@vercel/node" },
    { "src": "package.json", "use": "@vercel/next" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/$1" }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
EOF
```

**Vercel API (for automation):**
```bash
# List projects via API
curl -s "https://api.vercel.com/v9/projects" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  | python3 -c "
import json,sys
for p in json.load(sys.stdin).get('projects',[]):
    print(f'{p[\"name\"]:>30} {p.get(\"framework\",\"N/A\"):>12}')"

# Trigger deployment via API
curl -s -X POST "https://api.vercel.com/v13/deployments" \
  -H "Authorization: Bearer $VERCEL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"my-project","gitSource":{"type":"github","repoId":"REPO_ID","ref":"main"}}'
```

**Add a custom domain:**
```bash
vercel domains add myapp.com
vercel alias set DEPLOYMENT_URL myapp.com
```

## Output contract
- stdout: deployment URL or command output
- exit_code 0: success
- exit_code 1: build error, auth failure, or config issue

## Evaluate output
If build fails: check the build logs with `vercel logs`.
If 401: run `vercel login` or check VERCEL_TOKEN.
Preview URLs are auto-generated for every push — use `--prod` for production.
