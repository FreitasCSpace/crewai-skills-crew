# Skill: write_report

## Purpose
Produce a well-structured markdown report from data or analysis results and save it to ./output/report.md.

## When to use
- Summarising the results of any task for a human reader
- Producing a final deliverable after processing or analysis
- Creating structured documentation

## How to execute

**Build report dynamically from data (recommended):**
```bash
python3 -c "
import json
from datetime import datetime

# Load your data — adjust paths/fields as needed
with open('summary.json') as f:
    summary = json.load(f)

lines = [
    '# Task Report',
    f'*Generated: {datetime.now().strftime(\"%Y-%m-%d %H:%M\")}*',
    '',
    '## Summary',
]

# Add each key from summary as a bullet
for k, v in summary.items():
    lines.append(f'- **{k}**: {v}')

lines += ['', '## Details', '*(add detail sections as needed)*', '', '## Conclusion', 'Task completed successfully.']

import os
os.makedirs('../output', exist_ok=True)
with open('../output/report.md', 'w') as f:
    f.write('\n'.join(lines))
print(f'Report written: {len(lines)} lines')
"
```

**Write report with a markdown table:**
```bash
python3 -c "
import json
from datetime import datetime

with open('data.json') as f:
    records = json.load(f)

lines = [
    '# Report',
    f'*{datetime.now().strftime(\"%Y-%m-%d %H:%M\")}*',
    '',
    '## Data',
    '',
    '| # | Name | Value |',
    '|---|------|-------|',
]

for i, r in enumerate(records, 1):
    lines.append(f'| {i} | {r[\"name\"]} | {r[\"value\"]} |')

import os
os.makedirs('../output', exist_ok=True)
with open('../output/report.md', 'w') as f:
    f.write('\n'.join(lines))
print('Report written.')
"
```

**Always verify after writing:**
```bash
cat ../output/report.md
```

## Output contract
- stdout: confirmation + line count
- exit_code 0: report written
- exit_code 1+: path error or permission issue — check ../output/ exists

## Evaluate output
Read the report back. Does it have all expected sections?
If content is missing or truncated — rewrite it. Do not call the task done with an incomplete report.
