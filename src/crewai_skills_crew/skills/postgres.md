# Skill: postgres

## Purpose
Manage PostgreSQL databases — create schemas, run queries, import/export data, and administer users.

## When to use
- Creating databases, tables, or indexes
- Running SQL queries for data retrieval or manipulation
- Importing/exporting CSV or SQL dumps
- Managing users and permissions
- Checking database health or performance

## Prerequisites
- `psql` installed: `brew install postgresql` or available via Docker
- Connection string or individual params (host, port, user, password, dbname)
- Use `DATABASE_URL` env var when possible: `postgres://user:pass@host:5432/dbname`

## How to execute

**Connect and run a single query:**
```bash
psql "$DATABASE_URL" -c "SELECT version();"
```

**Run a query file:**
```bash
psql "$DATABASE_URL" -f schema.sql
```

**List databases:**
```bash
psql "$DATABASE_URL" -c "\l"
```

**List tables:**
```bash
psql "$DATABASE_URL" -c "\dt"
```

**Describe a table:**
```bash
psql "$DATABASE_URL" -c "\d+ tablename"
```

**Create a table:**
```bash
psql "$DATABASE_URL" << 'SQL'
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
SQL
```

**Insert data:**
```bash
psql "$DATABASE_URL" << 'SQL'
INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com');
SQL
```

**Query data:**
```bash
psql "$DATABASE_URL" -c "SELECT * FROM users ORDER BY created_at DESC LIMIT 20;" --csv
```

**Export to CSV:**
```bash
psql "$DATABASE_URL" -c "\COPY (SELECT * FROM users) TO STDOUT WITH CSV HEADER" > ./output/users.csv
echo "Exported $(wc -l < ./output/users.csv) lines"
```

**Import from CSV:**
```bash
psql "$DATABASE_URL" -c "\COPY users (name, email) FROM './data/users.csv' WITH CSV HEADER"
```

**Dump and restore:**
```bash
# Full dump
pg_dump "$DATABASE_URL" > backup.sql

# Dump specific table
pg_dump "$DATABASE_URL" -t users > users_backup.sql

# Restore
psql "$DATABASE_URL" < backup.sql
```

**Create user and grant permissions:**
```bash
psql "$DATABASE_URL" << 'SQL'
CREATE USER readonly WITH PASSWORD 'readpass';
GRANT CONNECT ON DATABASE mydb TO readonly;
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
SQL
```

**Check active connections:**
```bash
psql "$DATABASE_URL" -c "SELECT pid, usename, application_name, state, query_start FROM pg_stat_activity WHERE state = 'active';"
```

**Table sizes:**
```bash
psql "$DATABASE_URL" -c "
SELECT tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables WHERE schemaname = 'public' ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;"
```

**Run via Python (when psql unavailable):**
```bash
pip install psycopg2-binary --quiet && python3 -c "
import psycopg2, os, csv
conn = psycopg2.connect(os.environ['DATABASE_URL'])
cur = conn.cursor()
cur.execute('SELECT * FROM users LIMIT 10')
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
print('|'.join(cols))
for r in rows:
    print('|'.join(str(x) for x in r))
conn.close()
"
```

## Output contract
- stdout: query results or status messages
- exit_code 0: success
- exit_code 1+: connection error, syntax error, or permission denied

## Evaluate output
If "connection refused": check host, port, and that PostgreSQL is running.
If "permission denied": check user privileges.
If "relation does not exist": verify table name and schema.
Always use `--csv` for machine-readable output.
