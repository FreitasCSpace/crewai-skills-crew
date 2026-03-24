# Skill: redis

## Purpose
Use Redis for caching, message queues, rate limiting, and session storage.

## When to use
- Caching API responses or expensive computations
- Implementing pub/sub messaging
- Managing distributed locks or counters
- Storing session state or leaderboards
- Task queue management

## Prerequisites
- Redis server running (locally or remote)
- `redis-cli` installed: `apt-get install -y redis-tools` or `pip install redis` (Python client)
- Or use Python: `pip install redis`
- `REDIS_URL` env var (e.g., `redis://localhost:6379/0`)

## How to execute

**Check connection:**
```bash
redis-cli -u "$REDIS_URL" ping
```

**Basic key/value operations:**
```bash
# Set a key
redis-cli -u "$REDIS_URL" SET "user:1:name" "Alice"

# Get a key
redis-cli -u "$REDIS_URL" GET "user:1:name"

# Set with expiration (seconds)
redis-cli -u "$REDIS_URL" SETEX "cache:api:data" 3600 '{"result":"cached"}'

# Delete a key
redis-cli -u "$REDIS_URL" DEL "user:1:name"

# Check if key exists
redis-cli -u "$REDIS_URL" EXISTS "user:1:name"
```

**Hash operations (objects):**
```bash
# Set hash fields
redis-cli -u "$REDIS_URL" HSET "user:1" name "Alice" email "alice@example.com" score 95

# Get all fields
redis-cli -u "$REDIS_URL" HGETALL "user:1"

# Get single field
redis-cli -u "$REDIS_URL" HGET "user:1" email
```

**List operations (queues):**
```bash
# Push to queue
redis-cli -u "$REDIS_URL" RPUSH "tasks" '{"id":1,"action":"process"}'
redis-cli -u "$REDIS_URL" RPUSH "tasks" '{"id":2,"action":"notify"}'

# Pop from queue (FIFO)
redis-cli -u "$REDIS_URL" LPOP "tasks"

# Queue length
redis-cli -u "$REDIS_URL" LLEN "tasks"
```

**Sorted sets (leaderboard):**
```bash
# Add scores
redis-cli -u "$REDIS_URL" ZADD "leaderboard" 100 "alice" 85 "bob" 92 "charlie"

# Get top 5
redis-cli -u "$REDIS_URL" ZREVRANGE "leaderboard" 0 4 WITHSCORES

# Get rank
redis-cli -u "$REDIS_URL" ZREVRANK "leaderboard" "alice"
```

**List all keys matching a pattern:**
```bash
redis-cli -u "$REDIS_URL" KEYS "user:*"
redis-cli -u "$REDIS_URL" KEYS "cache:*"
```

**Python client (recommended for complex operations):**
```bash
pip install redis --quiet && python3 -c "
import redis, os, json

r = redis.from_url(os.environ.get('REDIS_URL', 'redis://localhost:6379/0'))

# Cache a function result
cache_key = 'cache:report:summary'
cached = r.get(cache_key)
if cached:
    print('Cache HIT:', json.loads(cached))
else:
    result = {'total': 42, 'average': 7.5}  # Expensive computation
    r.setex(cache_key, 3600, json.dumps(result))
    print('Cache MISS, stored:', result)

# Counter
r.incr('page:views:home')
print('Page views:', r.get('page:views:home').decode())
"
```

**Pub/Sub:**
```bash
# Subscribe (in background)
redis-cli -u "$REDIS_URL" SUBSCRIBE "notifications" &

# Publish a message
redis-cli -u "$REDIS_URL" PUBLISH "notifications" "New user signed up"
```

**Server info:**
```bash
redis-cli -u "$REDIS_URL" INFO server | head -15
redis-cli -u "$REDIS_URL" INFO memory | grep "used_memory_human"
redis-cli -u "$REDIS_URL" DBSIZE
```

**Flush database (careful!):**
```bash
redis-cli -u "$REDIS_URL" FLUSHDB
```

## Output contract
- stdout: command result (OK, value, or integer)
- PONG = connected
- (nil) = key not found
- (integer) N = count/length result

## Evaluate output
If "Could not connect": check Redis is running and REDIS_URL is correct.
If (nil): key doesn't exist or has expired.
Always set TTL on cache keys to avoid unbounded memory growth.
Use KEYS sparingly in production — use SCAN for large databases.
