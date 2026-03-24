# Skill: nginx

## Purpose
Configure and manage Nginx as a web server, reverse proxy, or load balancer.

## When to use
- Setting up a reverse proxy for backend services
- Serving static files or SPAs
- Configuring SSL/TLS with Let's Encrypt
- Load balancing across multiple backends
- Setting up redirects, headers, or rate limiting

## Prerequisites
- Nginx installed: `apt-get install -y nginx` or `yum install -y nginx`
- Verify: `nginx -v`

## How to execute

**Basic reverse proxy:**
```bash
cat > /etc/nginx/sites-available/myapp << 'EOF'
server {
    listen 80;
    server_name myapp.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

**Serve static files (SPA):**
```bash
cat > /etc/nginx/sites-available/spa << 'EOF'
server {
    listen 80;
    server_name spa.example.com;
    root /var/www/spa/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
}
EOF
```

**SSL with Let's Encrypt:**
```bash
# Install certbot
apt install certbot python3-certbot-nginx -y

# Get certificate and auto-configure nginx
certbot --nginx -d myapp.example.com --non-interactive --agree-tos -m admin@example.com

# Auto-renewal
certbot renew --dry-run
```

**Load balancer:**
```bash
cat > /etc/nginx/sites-available/loadbalancer << 'EOF'
upstream backend {
    least_conn;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
```

**API gateway with rate limiting:**
```bash
cat > /etc/nginx/sites-available/api << 'EOF'
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    listen 80;
    server_name api.example.com;

    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /health {
        return 200 '{"status":"ok"}';
        add_header Content-Type application/json;
    }
}
EOF
```

**Test and manage:**
```bash
# Test configuration
nginx -t

# Reload (graceful)
systemctl reload nginx

# Restart
systemctl restart nginx

# Check status
systemctl status nginx

# View error log
tail -50 /var/log/nginx/error.log

# View access log
tail -50 /var/log/nginx/access.log
```

**CORS headers:**
```bash
# Add to location block:
cat << 'EOF'
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
    add_header Access-Control-Allow-Headers "Authorization, Content-Type";

    if ($request_method = OPTIONS) {
        return 204;
    }
EOF
```

**Security headers:**
```bash
cat << 'EOF'
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'" always;
EOF
```

## Output contract
- nginx -t: "syntax is ok" = config is valid
- exit_code 0: success
- exit_code 1: config syntax error or permission issue

## Evaluate output
Always run `nginx -t` before reloading — a bad config will take down the server.
If "address already in use": another process is on port 80/443.
If 502 Bad Gateway: the backend service isn't running or is on the wrong port.
Check `/var/log/nginx/error.log` for detailed error information.
