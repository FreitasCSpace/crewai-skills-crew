# Skill: notion_api

## Purpose
Manage Notion workspaces — pages, databases, blocks, and content via the Notion API.

## When to use
- Creating or updating Notion pages and databases
- Querying databases for records
- Adding content blocks (text, tables, to-do lists)
- Automating documentation or knowledge base updates
- Syncing data between systems and Notion

## Prerequisites
- `NOTION_API_KEY` env var (Internal integration token from https://www.notion.so/my-integrations)
- Integration must be shared with target pages/databases (click ••• → Connections → Add)
- API version header required: `Notion-Version: 2022-06-28`

## How to execute

**Search for pages or databases:**
```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "Meeting Notes", "filter": {"property": "object", "value": "page"}}' \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin).get('results',[]):
    title = ''
    for t in r.get('properties',{}).get('title',{}).get('title',[]):
        title += t.get('plain_text','')
    if not title:
        title = r.get('properties',{}).get('Name',{}).get('title',[{}])[0].get('plain_text','Untitled')
    print(f'{r[\"id\"]} {r[\"object\"]:>8} {title}')"
```

**Query a database:**
```bash
curl -s -X POST "https://api.notion.com/v1/databases/DATABASE_ID/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "In Progress"}},
    "sorts": [{"property": "Created", "direction": "descending"}],
    "page_size": 20
  }' \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin)['results']:
    props = r['properties']
    name = props.get('Name',{}).get('title',[{}])[0].get('plain_text','?')
    status = props.get('Status',{}).get('select',{})
    status_name = status.get('name','?') if status else '?'
    print(f'{r[\"id\"][:8]}... [{status_name:>12}] {name}')"
```

**Create a page in a database:**
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "DATABASE_ID"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Task"}}]},
      "Status": {"select": {"name": "To Do"}},
      "Priority": {"select": {"name": "High"}},
      "Due Date": {"date": {"start": "2025-12-31"}}
    },
    "children": [
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Description"}}]}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Task details go here."}}]}}
    ]
  }'
```

**Update a page:**
```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/PAGE_ID" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

**Add content blocks to a page:**
```bash
curl -s -X PATCH "https://api.notion.com/v1/blocks/PAGE_ID/children" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Results"}}]}},
      {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "Task completed successfully"}}]}},
      {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"text": {"content": "3 files generated"}}]}},
      {"object": "block", "type": "divider", "divider": {}},
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "See attached report for details."}}]}}
    ]
  }'
```

**Create a standalone page:**
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "PARENT_PAGE_ID"},
    "properties": {"title": {"title": [{"text": {"content": "Meeting Notes - Dec 2024"}}]}},
    "children": [
      {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "Agenda"}}]}},
      {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"text": {"content": "Review Q4 results"}}], "checked": false}},
      {"object": "block", "type": "to_do", "to_do": {"rich_text": [{"text": {"content": "Discuss Q1 plans"}}], "checked": false}}
    ]
  }'
```

**List databases:**
```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "object", "value": "database"}}' \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin)['results']:
    title = r.get('title',[{}])[0].get('plain_text','Untitled')
    print(f'{r[\"id\"]} {title}')"
```

## Output contract
- stdout: JSON response
- HTTP 200: success
- HTTP 401: invalid integration token
- HTTP 404: page/database not found or not shared with integration
- HTTP 400: validation error (wrong property types)

## Evaluate output
If 401: check NOTION_API_KEY is valid.
If 404: make sure the integration is connected to the page/database in Notion.
Property types must match the database schema exactly (title, select, date, etc.).
