# Skill: run_python

## Purpose
Execute Python for computation, data processing, transformation, or analysis.

## When to use
- Processing structured data (JSON, CSV, text)
- Aggregation, sorting, filtering, statistics
- Generating formatted output — markdown tables, reports, charts
- Any logic beyond a simple bash one-liner
- Installing and using Python packages

## How to execute

**Inline script:**
```bash
python3 -c "
import json

with open('data.json') as f:
    data = json.load(f)

for i, r in enumerate(sorted(data, key=lambda x: x['score'], reverse=True)[:5], 1):
    print(f'{i}. {r[\"name\"]}: {r[\"score\"]}')
"
```

**Inspect data structure first (do this before processing):**
```bash
python3 -c "
import json
with open('data.json') as f:
    data = json.load(f)
print(type(data))
if isinstance(data, list) and data:
    print('Keys:', list(data[0].keys()))
    print('Sample:', data[0])
"
```

**Install a package then use it:**
```bash
pip install pandas --quiet && python3 -c "
import pandas as pd
df = pd.read_csv('data.csv')
print(df.describe())
"
```

**Write results to a file:**
```bash
python3 -c "
import json

with open('input.json') as f:
    data = json.load(f)

summary = {'count': len(data), 'total': sum(x['value'] for x in data)}

with open('summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
print('Saved:', summary)
"
```

## Output contract
- stdout: whatever you print
- exit_code 0: success
- exit_code 1: Python exception — full traceback in stderr

## Evaluate output
- Last line of stderr = the actual error if exit_code is 1
- If KeyError: inspect data structure first with the snippet above
- Fix and retry — never stop after one failure
- Always print a confirmation so you know the script finished
