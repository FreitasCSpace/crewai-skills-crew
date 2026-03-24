# Skill: validate_data

## Purpose
Validate JSON files, CSV files, and general data for correctness, completeness, and schema compliance.

## When to use
- After generating or receiving data files, before using them downstream
- When verifying required fields, data types, value ranges, or row counts
- When checking for nulls, empties, duplicates, or format violations

## How to execute

**Validate JSON is well-formed and inspect structure:**
```bash
python3 -c "
import json, sys
try:
    with open('data.json') as f:
        data = json.load(f)
    kind = type(data).__name__
    if isinstance(data, list):
        print(f'VALID JSON list — {len(data)} records')
        if data:
            print('Keys:', list(data[0].keys()))
    elif isinstance(data, dict):
        print(f'VALID JSON object — keys: {list(data.keys())}')
except json.JSONDecodeError as e:
    print(f'INVALID JSON: {e}')
    sys.exit(1)
"
```

**Validate required fields in JSON records:**
```bash
python3 -c "
import json, sys
required = ['id', 'name', 'value']   # ← adjust to your schema
with open('data.json') as f:
    data = json.load(f)
errors = []
for i, rec in enumerate(data):
    for field in required:
        if field not in rec:
            errors.append(f'Record {i}: missing \"{field}\"')
        elif rec[field] is None or rec[field] == '':
            errors.append(f'Record {i}: \"{field}\" is null/empty')
if errors:
    print('VALIDATION FAILED:')
    for e in errors: print(' -', e)
    sys.exit(1)
print(f'ALL {len(data)} RECORDS VALID')
"
```

**Validate CSV headers and rows:**
```bash
python3 -c "
import csv, sys
required_headers = ['name', 'score']  # ← adjust to your schema
with open('data.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
missing_headers = [h for h in required_headers if h not in reader.fieldnames]
if missing_headers:
    print(f'MISSING HEADERS: {missing_headers}')
    sys.exit(1)
empties = [(i+1, k) for i, row in enumerate(rows) for k, v in row.items() if not v or not v.strip()]
if empties:
    print('EMPTY CELLS:', empties[:10])
    sys.exit(1)
print(f'CSV VALID — {len(rows)} rows, headers: {reader.fieldnames}')
"
```

**Validate numeric ranges:**
```bash
python3 -c "
import json, sys
with open('data.json') as f:
    data = json.load(f)
errors = []
for i, rec in enumerate(data):
    score = rec.get('score', None)
    if not isinstance(score, (int, float)):
        errors.append(f'Record {i}: score is not a number ({score!r})')
    elif not (0 <= score <= 100):
        errors.append(f'Record {i}: score {score} out of range [0, 100]')
if errors:
    for e in errors: print(e)
    sys.exit(1)
print('All scores valid.')
"
```

## Output contract
- stdout: validation result message
- exit_code 0: validation passed
- exit_code 1: validation failed — message explains what's wrong

## Evaluate output
If exit_code 1: read the error, fix the data using file_ops or run_python, then re-validate.
Never proceed to the next step with invalid data.
