# Skill: write_markdown_report

## Purpose
Produce a well-structured markdown report and save it to ./output/report.md.

## When to use
- Final step to summarise results for a human reader
- When you have processed data and need a clean written output

## How to execute

Build report content in Python (best approach for dynamic data):
```bash
python3 -c "
import json
from datetime import datetime

with open('./data/summary.json') as f:
    summary = json.load(f)

with open('./data/records.json') as f:
    records = json.load(f)

lines = [
    '# Data Generation & Validation Report',
    f'Generated: {datetime.now().strftime(\"%Y-%m-%d %H:%M\")}',
    '',
    '## Summary',
    f'- Total records: **{summary[\"count\"]}**',
    f'- Average score: **{summary[\"average_score\"]}**',
    f'- Top scorer: **{summary[\"top_scorer\"]}**',
    '',
    '## Records',
    '',
    '| # | Name | Score |',
    '|---|------|-------|',
]

for i, r in enumerate(sorted(records, key=lambda x: x['score'], reverse=True), 1):
    lines.append(f'| {i} | {r[\"name\"]} | {r[\"score\"]} |')

lines += ['', '## Conclusion', 'All files generated and validated successfully.']

import os
os.makedirs('./output', exist_ok=True)
with open('./output/report.md', 'w') as f:
    f.write('\n'.join(lines))

print('Report written to ./output/report.md')
print(f'Lines: {len(lines)}')
"
```

## Output contract
- stdout: confirmation message
- exit_code 0: report written
- exit_code 1+: error writing — check path and directory exists

## Evaluate output
Always read the report back to confirm it looks correct:
```bash
cat ./output/report.md
```
