# Skill: react

## Purpose
Build React web applications — components, hooks, routing, state management, and deployment.

## When to use
- Creating new React projects (Vite, Next.js, CRA)
- Building UI components, pages, and layouts
- Implementing state management, routing, or API calls
- Generating React code from specifications

## Prerequisites
- Node.js 18+ installed
- Verify: `node --version && npm --version`

## How to execute

**Create a new React project (Vite):**
```bash
npm create vite@latest my-app -- --template react-ts
cd my-app && npm install
```

**Create a Next.js project:**
```bash
npx create-next-app@latest my-app --typescript --tailwind --app --eslint
cd my-app && npm install
```

**Install common dependencies:**
```bash
npm install react-router-dom @tanstack/react-query axios zustand
npm install -D tailwindcss @types/react @types/react-dom
```

**Create a component:**
```bash
mkdir -p src/components

cat > src/components/UserCard.tsx << 'EOF'
interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
}

export function UserCard({ name, email, avatar }: UserCardProps) {
  return (
    <div className="flex items-center gap-4 p-4 rounded-lg border">
      {avatar && <img src={avatar} alt={name} className="w-12 h-12 rounded-full" />}
      <div>
        <h3 className="font-semibold text-lg">{name}</h3>
        <p className="text-gray-500">{email}</p>
      </div>
    </div>
  );
}
EOF
```

**Create a page with data fetching:**
```bash
cat > src/pages/UsersPage.tsx << 'EOF'
import { useEffect, useState } from 'react';
import { UserCard } from '../components/UserCard';

interface User {
  id: number;
  name: string;
  email: string;
}

export function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => { setUsers(data); setLoading(false); })
      .catch(err => { console.error(err); setLoading(false); });
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div className="space-y-4 p-8">
      <h1 className="text-2xl font-bold">Users</h1>
      {users.map(user => (
        <UserCard key={user.id} name={user.name} email={user.email} />
      ))}
    </div>
  );
}
EOF
```

**Create a custom hook:**
```bash
cat > src/hooks/useApi.ts << 'EOF'
import { useState, useEffect } from 'react';

export function useApi<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(url)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(setData)
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}
EOF
```

**Create a form with state:**
```bash
cat > src/components/ContactForm.tsx << 'EOF'
import { useState, FormEvent } from 'react';

export function ContactForm() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    if (res.ok) setSubmitted(true);
  };

  if (submitted) return <p className="text-green-600">Thank you!</p>;

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
      <input
        type="text" placeholder="Name" required
        value={form.name} onChange={e => setForm({ ...form, name: e.target.value })}
        className="w-full p-2 border rounded"
      />
      <input
        type="email" placeholder="Email" required
        value={form.email} onChange={e => setForm({ ...form, email: e.target.value })}
        className="w-full p-2 border rounded"
      />
      <textarea
        placeholder="Message" required rows={4}
        value={form.message} onChange={e => setForm({ ...form, message: e.target.value })}
        className="w-full p-2 border rounded"
      />
      <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">Send</button>
    </form>
  );
}
EOF
```

**Set up React Router:**
```bash
cat > src/App.tsx << 'EOF'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { UsersPage } from './pages/UsersPage';

function App() {
  return (
    <BrowserRouter>
      <nav className="p-4 bg-gray-100">
        <Link to="/" className="mr-4">Home</Link>
        <Link to="/users">Users</Link>
      </nav>
      <Routes>
        <Route path="/" element={<h1 className="p-8 text-2xl">Home</h1>} />
        <Route path="/users" element={<UsersPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
EOF
```

**Build for production:**
```bash
npm run build
ls -la dist/
```

## Output contract
- stdout: build output or dev server URL
- exit_code 0: success
- exit_code 1: build/type error

## Evaluate output
If type errors: check prop interfaces and imports.
If "Module not found": run `npm install` and check import paths.
Always run `npm run build` to verify before deploying.
