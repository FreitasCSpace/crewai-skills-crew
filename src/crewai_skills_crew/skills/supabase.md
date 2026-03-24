# Skill: supabase

## Purpose
Interact with Supabase (Postgres + Auth + Storage + Realtime) via the REST API or Python client.

## When to use
- CRUD operations on Supabase tables (PostgREST)
- Managing user authentication (sign up, sign in, tokens)
- Uploading/downloading files to Supabase Storage
- Running RPC functions (server-side Postgres functions)
- When building backends on Supabase

## Prerequisites
- `SUPABASE_URL` env var (e.g., `https://abc123.supabase.co`)
- `SUPABASE_ANON_KEY` or `SUPABASE_SERVICE_KEY` env var
- Service key has full access; anon key respects Row Level Security (RLS)

## How to execute

**Select rows (GET):**
```bash
curl -s "$SUPABASE_URL/rest/v1/users?select=id,name,email&limit=20" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  | python3 -m json.tool
```

**Filter and order:**
```bash
curl -s "$SUPABASE_URL/rest/v1/users?select=*&status=eq.active&order=created_at.desc&limit=10" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  | python3 -m json.tool
```

**Insert a row (POST):**
```bash
curl -s -X POST "$SUPABASE_URL/rest/v1/users" \
  -H "apikey: $SUPABASE_SERVICE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"name": "Alice", "email": "alice@example.com", "status": "active"}'
```

**Update a row (PATCH):**
```bash
curl -s -X PATCH "$SUPABASE_URL/rest/v1/users?id=eq.42" \
  -H "apikey: $SUPABASE_SERVICE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"status": "inactive"}'
```

**Delete a row:**
```bash
curl -s -X DELETE "$SUPABASE_URL/rest/v1/users?id=eq.42" \
  -H "apikey: $SUPABASE_SERVICE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_KEY"
```

**Call an RPC function:**
```bash
curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/get_user_stats" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 42}' \
  | python3 -m json.tool
```

**Upload a file to Storage:**
```bash
curl -s -X POST "$SUPABASE_URL/storage/v1/object/BUCKET_NAME/path/to/file.pdf" \
  -H "apikey: $SUPABASE_SERVICE_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
  -H "Content-Type: application/pdf" \
  --data-binary @./output/report.pdf
```

**Download a file from Storage:**
```bash
curl -s "$SUPABASE_URL/storage/v1/object/public/BUCKET_NAME/path/to/file.pdf" \
  -o ./data/downloaded.pdf
```

**Python client (recommended for complex operations):**
```bash
pip install supabase --quiet && python3 -c "
import os
from supabase import create_client

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_SERVICE_KEY']
supabase = create_client(url, key)

# Select
result = supabase.table('users').select('*').limit(10).execute()
for r in result.data:
    print(r)

# Insert
result = supabase.table('users').insert({'name': 'Bob', 'email': 'bob@example.com'}).execute()
print(f'Inserted: {result.data}')
"
```

**Auth — sign up a user:**
```bash
curl -s -X POST "$SUPABASE_URL/auth/v1/signup" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'
```

## PostgREST filter operators
- `eq` = equals, `neq` = not equals
- `gt`, `gte`, `lt`, `lte` = comparisons
- `like`, `ilike` = pattern matching
- `in` = value in list: `status=in.(active,pending)`
- `is` = null check: `deleted_at=is.null`

## Output contract
- stdout: JSON response or file content
- HTTP 200/201: success
- HTTP 401: invalid or expired key
- HTTP 404: table or function not found
- HTTP 409: unique constraint violation

## Evaluate output
If 401: check that the correct key is used (service key bypasses RLS).
If empty result: check RLS policies — they may block the anon key.
If 404: verify table name matches exactly (case-sensitive).
