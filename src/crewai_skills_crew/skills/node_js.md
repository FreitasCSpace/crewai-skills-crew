# Skill: node_js

## Purpose
Build, run, and manage Node.js/TypeScript applications and packages.

## When to use
- Creating Node.js applications or scripts
- Installing and managing npm packages
- Running Express, Fastify, or Next.js servers
- Building TypeScript projects
- Running JavaScript for data processing when Python isn't preferred

## Prerequisites
- Node.js installed: `brew install node` or via `nvm`
- Verify: `node --version && npm --version`

## How to execute

**Initialize a project:**
```bash
mkdir -p myapp && cd myapp
npm init -y
```

**Install packages:**
```bash
npm install express dotenv cors
npm install -D typescript @types/node @types/express ts-node nodemon
```

**Create a simple Express server:**
```bash
cat > index.js << 'EOF'
const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
  res.json({ status: 'ok', message: 'Server is running' });
});

app.get('/api/data', (req, res) => {
  res.json({ items: [{ id: 1, name: 'Item 1' }] });
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
EOF
node index.js &
```

**Run a one-off script:**
```bash
node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('data.json', 'utf-8'));
console.log('Records:', data.length);
const total = data.reduce((sum, r) => sum + r.value, 0);
console.log('Total:', total);
"
```

**TypeScript setup:**
```bash
npx tsc --init --strict --outDir dist --rootDir src
mkdir -p src

cat > src/index.ts << 'EOF'
interface User {
  id: number;
  name: string;
  email: string;
}

const users: User[] = [
  { id: 1, name: 'Alice', email: 'alice@example.com' },
  { id: 2, name: 'Bob', email: 'bob@example.com' },
];

console.log(JSON.stringify(users, null, 2));
EOF

npx tsc && node dist/index.js
```

**Process a file with Node:**
```bash
node -e "
const fs = require('fs');
const csv = fs.readFileSync('data.csv', 'utf-8')
  .trim().split('\n')
  .map(line => line.split(','));

const [headers, ...rows] = csv;
console.log('Headers:', headers);
console.log('Rows:', rows.length);

// Convert to JSON
const data = rows.map(r => Object.fromEntries(headers.map((h, i) => [h, r[i]])));
fs.writeFileSync('./output/data.json', JSON.stringify(data, null, 2));
console.log('Converted to JSON');
"
```

**Package.json scripts:**
```bash
node -e "
const pkg = require('./package.json');
pkg.scripts = {
  start: 'node index.js',
  dev: 'nodemon index.js',
  build: 'tsc',
  test: 'jest'
};
require('fs').writeFileSync('package.json', JSON.stringify(pkg, null, 2));
console.log('Scripts added');
"
```

**HTTP requests with fetch (Node 18+):**
```bash
node -e "
(async () => {
  const res = await fetch('https://api.example.com/data');
  const data = await res.json();
  console.log(JSON.stringify(data, null, 2));
})();
"
```

**Check for outdated packages:**
```bash
npm outdated
```

**Run tests:**
```bash
npx jest --verbose
```

## Output contract
- stdout: script output
- exit_code 0: success
- exit_code 1: JavaScript error (stack trace on stderr)

## Evaluate output
If "Cannot find module": run `npm install` first.
If TypeScript errors: check `tsconfig.json` and fix type issues.
Always check `node --version` — some features require Node 18+.
