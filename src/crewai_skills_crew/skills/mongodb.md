# Skill: mongodb

## Purpose
Manage MongoDB databases — CRUD operations, aggregation, indexing, and administration.

## When to use
- Creating collections and inserting documents
- Querying, filtering, and aggregating data
- Managing indexes for performance
- Exporting/importing data
- Database administration tasks

## Prerequisites
- `mongosh` (MongoDB Shell) or `mongoimport`/`mongoexport` tools installed
- Or Python: `pip install pymongo`
- `MONGODB_URI` env var (e.g., `mongodb://localhost:27017/mydb` or Atlas connection string)

## How to execute

**Connect and check:**
```bash
mongosh "$MONGODB_URI" --eval "db.stats()"
```

**Insert documents:**
```bash
mongosh "$MONGODB_URI" --eval '
db.users.insertMany([
  { name: "Alice", email: "alice@example.com", age: 30, tags: ["admin", "user"] },
  { name: "Bob", email: "bob@example.com", age: 25, tags: ["user"] },
  { name: "Charlie", email: "charlie@example.com", age: 35, tags: ["user", "editor"] }
])
'
```

**Query documents:**
```bash
# Find all
mongosh "$MONGODB_URI" --eval 'db.users.find().toArray()' --quiet

# Find with filter
mongosh "$MONGODB_URI" --eval 'db.users.find({ age: { $gte: 30 } }).toArray()' --quiet

# Find with projection
mongosh "$MONGODB_URI" --eval 'db.users.find({}, { name: 1, email: 1, _id: 0 }).toArray()' --quiet

# Find one
mongosh "$MONGODB_URI" --eval 'db.users.findOne({ email: "alice@example.com" })' --quiet
```

**Update documents:**
```bash
# Update one
mongosh "$MONGODB_URI" --eval '
db.users.updateOne(
  { email: "alice@example.com" },
  { $set: { age: 31, updatedAt: new Date() } }
)'

# Update many
mongosh "$MONGODB_URI" --eval '
db.users.updateMany(
  { tags: "user" },
  { $set: { active: true } }
)'
```

**Delete documents:**
```bash
mongosh "$MONGODB_URI" --eval 'db.users.deleteOne({ email: "bob@example.com" })'
```

**Aggregation pipeline:**
```bash
mongosh "$MONGODB_URI" --eval '
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { _id: "$customerId", total: { $sum: "$amount" }, count: { $sum: 1 } } },
  { $sort: { total: -1 } },
  { $limit: 10 }
]).toArray()
' --quiet
```

**Create indexes:**
```bash
mongosh "$MONGODB_URI" --eval '
db.users.createIndex({ email: 1 }, { unique: true })
db.users.createIndex({ name: "text" })
db.orders.createIndex({ customerId: 1, createdAt: -1 })
'

# List indexes
mongosh "$MONGODB_URI" --eval 'db.users.getIndexes()' --quiet
```

**Export/Import:**
```bash
# Export to JSON
mongoexport --uri="$MONGODB_URI" --collection=users --out=./output/users.json --jsonArray

# Import from JSON
mongoimport --uri="$MONGODB_URI" --collection=users --file=./data/users.json --jsonArray

# Export to CSV
mongoexport --uri="$MONGODB_URI" --collection=users --type=csv --fields=name,email,age --out=./output/users.csv
```

**Python (PyMongo — recommended for complex operations):**
```bash
pip install pymongo --quiet && python3 -c "
from pymongo import MongoClient
import os, json

client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_default_database()

# Query
users = list(db.users.find({}, {'_id': 0, 'name': 1, 'email': 1}).limit(10))
for u in users:
    print(f'{u[\"name\"]:>15} {u[\"email\"]}')

# Count
print(f'Total users: {db.users.count_documents({})}')

# Aggregate
pipeline = [
    {'\$group': {'_id': None, 'avgAge': {'\$avg': '\$age'}}},
]
result = list(db.users.aggregate(pipeline))
print(f'Average age: {result[0][\"avgAge\"]:.1f}')

client.close()
"
```

**List collections:**
```bash
mongosh "$MONGODB_URI" --eval 'db.getCollectionNames()' --quiet
```

**Database stats:**
```bash
mongosh "$MONGODB_URI" --eval '
const stats = db.stats();
print("Collections:", stats.collections);
print("Documents:", stats.objects);
print("Size:", (stats.dataSize / 1024 / 1024).toFixed(2), "MB");
' --quiet
```

## Output contract
- stdout: query results or operation confirmation
- exit_code 0: success
- exit_code 1+: connection error, query error, or auth failure

## Evaluate output
If "MongoNetworkError": check connection string and network access (Atlas whitelist).
If "E11000 duplicate key": unique index violation — document with same key exists.
Use `--quiet` flag with mongosh to suppress the shell banner.
For Atlas: ensure your IP is in the access list.
