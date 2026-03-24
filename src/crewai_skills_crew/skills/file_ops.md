# Skill: file_ops

## Purpose
Read, write, list, copy, move, and delete files and directories.

## When to use
- Reading input files or inspecting existing content
- Writing outputs, reports, configs, or data files
- Listing directory contents to discover what exists
- Verifying a file was written correctly after creating it

## How to execute

**List files:**
```bash
find . -type f | sort
ls -la
```

**Read a file:**
```bash
cat filename.txt
head -n 50 filename.txt
```

**Write a file (multiline):**
```bash
cat > output.md << 'EOF'
# Title
Content here.
EOF
```

**Write dynamically with Python:**
```bash
python3 -c "
content = 'your content'
with open('output.txt', 'w') as f:
    f.write(content)
print('Written.')
"
```

**Check file exists and is non-empty:**
```bash
[ -s filename.txt ] && echo "EXISTS AND NON-EMPTY" || echo "MISSING OR EMPTY"
```

**Copy / move / delete:**
```bash
cp source.txt dest.txt
mv old.txt new.txt
rm unwanted.txt
mkdir -p subdir/
```

## Output contract
- stdout: file contents or confirmation message
- exit_code 0: success
- exit_code 1+: not found, permission error, or bad path

## Evaluate output
Always read a file back after writing to confirm content is correct.
If a file is missing or empty when expected — stop and investigate.
