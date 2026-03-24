# Skill: fastapi

## Purpose
Build REST APIs with Python FastAPI — endpoints, models, database integration, and deployment.

## When to use
- Creating Python web APIs quickly
- Building CRUD endpoints with automatic OpenAPI docs
- Integrating with databases (SQLAlchemy, SQLModel)
- Creating webhook receivers or microservices

## Prerequisites
- Python 3.9+
- Install: `pip install fastapi uvicorn`

## How to execute

**Create a basic API:**
```bash
pip install fastapi uvicorn --quiet

cat > main.py << 'EOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title="My API", version="1.0.0")

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

items_db: dict[int, Item] = {}
next_id = 1

@app.get("/")
def root():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

@app.get("/items")
def list_items():
    return [{"id": k, **v.model_dump()} for k, v in items_db.items()]

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items_db[item_id].model_dump()}

@app.post("/items", status_code=201)
def create_item(item: Item):
    global next_id
    items_db[next_id] = item
    result = {"id": next_id, **item.model_dump()}
    next_id += 1
    return result

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return {"id": item_id, **item.model_dump()}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"deleted": item_id}
EOF
```

**Run the server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
echo "API docs: http://localhost:8000/docs"
```

**Create with SQLModel (database):**
```bash
pip install sqlmodel aiosqlite --quiet

cat > main.py << 'EOF'
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    active: bool = True

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

app = FastAPI()

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/users")
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()

@app.post("/users", status_code=201)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
EOF
```

**Add authentication middleware:**
```bash
cat > auth.py << 'EOF'
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    import os
    if x_api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
EOF
```

**Test the API:**
```bash
# Health check
curl -s http://localhost:8000/ | python3 -m json.tool

# Create item
curl -s -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Widget","price":9.99}' | python3 -m json.tool

# List items
curl -s http://localhost:8000/items | python3 -m json.tool
```

**Generate requirements.txt:**
```bash
pip freeze | grep -iE "fastapi|uvicorn|sqlmodel|pydantic" > requirements.txt
cat requirements.txt
```

**Create a Dockerfile:**
```bash
cat > Dockerfile << 'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

## Output contract
- stdout: server logs or curl responses
- exit_code 0: success
- exit_code 1: import error, validation error, or port in use

## Evaluate output
If "Address already in use": kill the existing process or use a different port.
If validation error: check Pydantic model — all required fields must be in the request.
API docs are auto-generated at `/docs` (Swagger) and `/redoc`.
