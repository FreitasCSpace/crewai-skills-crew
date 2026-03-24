# Skill: read_file

## Purpose
Read and inspect the contents of any file on disk.

## When to use
- Verifying a file was written correctly
- Reading input data before processing
- Inspecting file contents at any point in the workflow

## How to execute

Read full file:
```bash
cat ./path/to/file.txt
```

Read JSON and pretty-print:
```bash
cat ./data/records.json | python3 -m json.tool
```

Read first N lines:
```bash
head -n 20 ./data/records.json
```

Check file exists and has content:
```bash
[ -s ./data/records.json ] && echo "EXISTS AND NON-EMPTY" || echo "MISSING OR EMPTY"
```

List all files in a directory:
```bash
find ./data -type f | sort
find ./output -type f | sort
```

## Output contract
- stdout: file contents
- exit_code 0: success
- exit_code 1+: file not found or unreadable

## Evaluate output
Does the content look correct, complete, and non-empty?
If missing or empty — stop and determine why before continuing.
