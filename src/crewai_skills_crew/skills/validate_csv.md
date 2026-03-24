# Skill: validate_csv

## Purpose
Validate that a CSV file is well-formed, has the expected headers, and contains clean data.

## When to use
- After generating a CSV file, before it is used downstream
- When you need to confirm headers and row counts
- When you need to check for missing values or type issues

## How to execute

Check file exists and has rows:
```bash
python3 -c "
import csv, sys
with open('./data/scores.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
print(f'Headers: {reader.fieldnames}')
print(f'Rows: {len(rows)}')
if len(rows) == 0:
    print('ERROR: no data rows')
    sys.exit(1)
"
```

Check required headers exist:
```bash
python3 -c "
import csv, sys
required_headers = ['name', 'score']   # adjust to your schema
with open('./data/scores.csv') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

missing = [h for h in required_headers if h not in reader.fieldnames]
if missing:
    print(f'MISSING HEADERS: {missing}')
    sys.exit(1)
else:
    print(f'Headers OK: {reader.fieldnames}')
    print(f'Row count: {len(rows)}')
"
```

Check for empty cells:
```bash
python3 -c "
import csv, sys
issues = []
with open('./data/scores.csv') as f:
    for i, row in enumerate(csv.DictReader(f)):
        for k, v in row.items():
            if not v or not v.strip():
                issues.append(f'Row {i+1}, column \"{k}\": empty value')
if issues:
    for issue in issues:
        print(issue)
    sys.exit(1)
else:
    print('No empty cells found.')
"
```

## Output contract
- stdout: validation result
- exit_code 0: passed
- exit_code 1: failed — error message explains the problem

## Evaluate output
If validation fails: fix the source data using write_file skill, then re-validate.
