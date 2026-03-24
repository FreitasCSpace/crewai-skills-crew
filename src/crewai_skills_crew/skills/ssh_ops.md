# Skill: ssh_ops

## Purpose
Execute remote commands, transfer files, and manage servers via SSH.

## When to use
- Running commands on remote servers
- Transferring files between local and remote machines
- Setting up SSH tunnels for database or service access
- Managing SSH keys and configurations
- Automating server maintenance tasks

## Prerequisites
- SSH client installed (built into macOS/Linux)
- SSH key or password access to target server
- `SSH_HOST`, `SSH_USER` env vars (optional, for convenience)

## How to execute

**Run a remote command:**
```bash
ssh "$SSH_USER@$SSH_HOST" "hostname && uptime && df -h /"
```

**Run a script remotely:**
```bash
ssh "$SSH_USER@$SSH_HOST" << 'REMOTE'
echo "=== System Info ==="
uname -a
echo "=== Memory ==="
free -h
echo "=== Disk ==="
df -h
echo "=== Docker containers ==="
docker ps --format "table {{.Names}}\t{{.Status}}" 2>/dev/null || echo "Docker not installed"
REMOTE
```

**Copy files — SCP:**
```bash
# Upload a file
scp ./output/report.md "$SSH_USER@$SSH_HOST:/home/$SSH_USER/reports/"

# Download a file
scp "$SSH_USER@$SSH_HOST:/var/log/app.log" ./data/remote_app.log

# Upload a directory
scp -r ./output/ "$SSH_USER@$SSH_HOST:/home/$SSH_USER/output/"
```

**Copy files — rsync (better for large or incremental transfers):**
```bash
# Sync local to remote
rsync -avz --progress ./output/ "$SSH_USER@$SSH_HOST:/home/$SSH_USER/output/"

# Sync remote to local
rsync -avz "$SSH_USER@$SSH_HOST:/var/log/app/" ./data/logs/

# Dry run (see what would be transferred)
rsync -avzn ./output/ "$SSH_USER@$SSH_HOST:/home/$SSH_USER/output/"
```

**SSH tunnel (port forwarding):**
```bash
# Forward remote PostgreSQL to local port
ssh -L 5433:localhost:5432 "$SSH_USER@$SSH_HOST" -N -f
# Now connect locally: psql -h localhost -p 5433

# Forward remote Redis to local
ssh -L 6380:localhost:6379 "$SSH_USER@$SSH_HOST" -N -f

# Forward remote web service
ssh -L 8080:localhost:3000 "$SSH_USER@$SSH_HOST" -N -f
```

**Generate SSH key:**
```bash
ssh-keygen -t ed25519 -C "automation@crew" -f ~/.ssh/id_crew -N ""
echo "Public key:"
cat ~/.ssh/id_crew.pub
```

**Copy SSH key to server:**
```bash
ssh-copy-id -i ~/.ssh/id_crew "$SSH_USER@$SSH_HOST"
```

**SSH config file:**
```bash
cat >> ~/.ssh/config << 'EOF'

Host myserver
    HostName 192.168.1.100
    User deploy
    IdentityFile ~/.ssh/id_crew
    Port 22
    StrictHostKeyChecking no
EOF

# Now just: ssh myserver
```

**Run command on multiple servers:**
```bash
for host in server1 server2 server3; do
    echo "=== $host ==="
    ssh "$SSH_USER@$host" "uptime && docker ps --format '{{.Names}}: {{.Status}}'" 2>&1
    echo ""
done
```

**Check server health:**
```bash
ssh "$SSH_USER@$SSH_HOST" << 'REMOTE'
echo "Host: $(hostname)"
echo "Uptime: $(uptime -p 2>/dev/null || uptime)"
echo "Load: $(cat /proc/loadavg | awk '{print $1, $2, $3}')"
echo "Memory: $(free -h | awk '/Mem:/ {print $3 "/" $2}')"
echo "Disk: $(df -h / | awk 'NR==2 {print $3 "/" $2 " (" $5 ")"}')"
echo "Processes: $(ps aux | wc -l)"
REMOTE
```

**Deploy with SSH:**
```bash
ssh "$SSH_USER@$SSH_HOST" << 'REMOTE'
cd /opt/myapp
git pull origin main
docker compose down
docker compose up -d --build
docker compose logs --tail 20
REMOTE
```

## Output contract
- stdout: remote command output
- exit_code 0: success
- exit_code 255: SSH connection failed
- exit_code 1: remote command failed

## Evaluate output
If "Connection refused": check host, port, and that SSH is running on the server.
If "Permission denied": check SSH key or password, and user permissions.
If "Host key verification failed": add `-o StrictHostKeyChecking=no` or update known_hosts.
Use `-v` flag for verbose SSH debugging.
