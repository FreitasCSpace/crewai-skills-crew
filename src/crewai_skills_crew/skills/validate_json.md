# Skill: validate_json

## Purpose
Validate that a JSON file is well-formed, has the expected structure, and passes content rules.

## When to use
- After generating or writing a JSON file, before passing it downstream
- When you need to confirm required fields exist
- When you need to check value types, ranges, or non-empty content

## How to execute

Check file is valid JSON:
```bash
python3 -c "
import json, sys
try:
    with open('./data/records.json') as f:
        data = json.load(f)
    print(f'VALID JSON — type: {type(data).__name__}')
    if isinstance(data, list):
        print(f'Records: {len(data)}')
    elif isinstance(data, dict):
        print(f'Keys: {list(data.keys())}')
except json.JSONDecodeError as e:
    print(f'INVALID JSON: {e}')
    sys.exit(1)
"
```

Check required fields exist in every record:
```bash
python3 -c "
import json, sys
required = ['id', 'name', 'score']   # adjust to your schema
with open('./data/records.json') as f:
    data = json.load(f)

errors = []
for i, record in enumerate(data):
    for field in required:
        if field not in record:
            errors.append(f'Record {i}: missing field \"{field}\"')

if errors:
    print('VALIDATION FAILED:')
    for e in errors:
        print(' -', e)
    sys.exit(1)
else:
    print(f'ALL {len(data)} RECORDS VALID — fields {required} present in all.')
"
```

Check no empty or null values:
```bash
python3 -c "
import json, sys
with open('./data/records.json') as f:
    data = json.load(f)

issues = []
for i, record in enumerate(data):
    for k, v in record.items():
        if v is None or v == '' or v == []:
            issues.append(f'Record {i}: field \"{k}\" is empty/null')

if issues:
    print('ISSUES FOUND:')
    for issue in issues:
        print(' -', issue)
    sys.exit(1)
else:
    print(f'No empty values found across {len(data)} records.')
"
```

## Output contract
- stdout: validation result message
- exit_code 0: validation passed
- exit_code 1: validation failed — stdout/stderr explains what's wrong

## Evaluate output
If exit_code is 1: read the error message, fix the file using write_file skill, then re-validate.
Never proceed to the next step with invalid data.
