# Skill: write_file

## Purpose
Write text content to a file on disk.

## When to use
- Creating output files, reports, configs, or data files
- Persisting generated content for another agent to consume
- Saving results to disk

## How to execute

Write multiline content with heredoc (best for structured content):
```bash
mkdir -p ./output && cat > ./output/myfile.txt << 'EOF'
line one
line two
line three
EOF
```

Write JSON using Python (best for structured data):
```bash
python3 -c "
import json
data = [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]
with open('./data/records.json', 'w') as f:
    json.dump(data, f, indent=2)
print('Written', len(data), 'records.')
"
```

Write a CSV:
```bash
python3 -c "
import csv
rows = [['name','score'], ['Alice','95'], ['Bob','87']]
with open('./data/scores.csv', 'w', newline='') as f:
    csv.writer(f).writerows(rows)
print('CSV written.')
"
```

## Output contract
- stdout: confirmation message (print one so you know it worked)
- exit_code 0: file written successfully
- exit_code 1+: directory doesn't exist or permission error

## Evaluate output
Always read the file back after writing to confirm content is correct:
```bash
cat ./output/myfile.txt
```
If content is missing or wrong — rewrite it. Do not proceed with bad data.
