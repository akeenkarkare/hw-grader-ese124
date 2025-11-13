# Judge0 Remote Server Setup Guide

This guide will help you set up Judge0 on a remote Linux server and configure your homework grader to use it.

## Prerequisites

- A Linux server (Ubuntu 20.04+ recommended)
- SSH access to the server
- Docker and Docker Compose installed on the server
- Port 2358 accessible (or configure firewall)

## Step 1: Install Docker on Linux Server

SSH into your server and run:

```bash
# Update packages
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add your user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
# Log out and back in for group changes to take effect
```

## Step 2: Set Up Judge0 on Server

```bash
# Create judge0 directory
mkdir -p ~/judge0
cd ~/judge0

# Download Judge0 configuration
wget https://github.com/judge0/judge0/releases/download/v1.13.0/judge0-v1.13.0.zip
unzip judge0-v1.13.0.zip
cd judge0-v1.13.0

# Or clone the repository
git clone https://github.com/judge0/judge0.git
cd judge0
```

## Step 3: Configure Judge0

Edit the `judge0.conf` file:

```bash
# Essential settings in judge0.conf:

# Redis (no password for simplicity)
REDIS_HOST=redis
REDIS_PORT=6379
# REDIS_PASSWORD= (leave commented out)

# PostgreSQL
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=judge0
POSTGRES_USER=judge0
POSTGRES_PASSWORD=YourStrongPassword123

# Optional: Increase limits for better performance
MAX_QUEUE_SIZE=500
CPU_TIME_LIMIT=5
MEMORY_LIMIT=256000
```

Edit `docker-compose.yml` to remove the Redis password requirement:

```yaml
  redis:
    image: redis:7.2.4
    command: ["redis-server", "--appendonly", "no"]
    restart: always
```

## Step 4: Start Judge0

```bash
cd ~/judge0/judge0-v1.13.0  # or wherever you extracted it

# Start Judge0
docker-compose up -d

# Check if it's running
docker-compose ps

# Check logs
docker-compose logs -f server
# Press Ctrl+C to exit logs
```

Wait about 30 seconds for Judge0 to fully initialize.

## Step 5: Test Judge0

```bash
# Test the Judge0 API (on the server)
curl http://localhost:2358/about

# Should return something like:
# {"version":"1.13.1","homepage":"https://judge0.com",...}
```

Test with a simple submission:

```bash
curl -X POST "http://localhost:2358/submissions?base64_encoded=true&wait=true" \
  -H "Content-Type: application/json" \
  -d '{
    "source_code": "I2luY2x1ZGUgPHN0ZGlvLmg+CgppbnQgbWFpbigpIHsKICAgIHByaW50ZigiSGVsbG8sIFdvcmxkISIpOwogICAgcmV0dXJuIDA7Cn0=",
    "language_id": 50,
    "stdin": ""
  }'
```

You should see output with `"stdout":"SGVsbG8sIFdvcmxkIQ==\n"` (base64 encoded "Hello, World!").

## Step 6: Configure Firewall (Important!)

Judge0 will be accessible on port 2358. You need to:

### Option A: Open Port to Your IP Only (Recommended)

```bash
# UFW (Ubuntu)
sudo ufw allow from YOUR_LOCAL_IP to any port 2358
sudo ufw status

# Or iptables
sudo iptables -A INPUT -p tcp -s YOUR_LOCAL_IP --dport 2358 -j ACCEPT
```

### Option B: Use SSH Tunnel (Most Secure)

Don't open the port at all. Instead, create an SSH tunnel from your Mac:

```bash
# On your Mac, create SSH tunnel:
ssh -L 2358:localhost:2358 user@your-server-ip -N

# Now Judge0 on remote server is accessible at localhost:2358 on your Mac
# Keep this terminal open while working
```

Then in your homework grader `.env`:
```bash
JUDGE0_MODE=self-hosted
JUDGE0_SELF_HOSTED_URL=http://localhost:2358
```

### Option C: Use Nginx Reverse Proxy with Auth (Production)

```bash
# Install nginx
sudo apt-get install nginx

# Create nginx config for Judge0
sudo nano /etc/nginx/sites-available/judge0

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:2358;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # Optional: Add basic auth
        auth_basic "Judge0 API";
        auth_basic_user_file /etc/nginx/.htpasswd;
    }
}

# Enable the site
sudo ln -s /etc/nginx/sites-available/judge0 /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Create password file (optional)
sudo apt-get install apache2-utils
sudo htpasswd -c /etc/nginx/.htpasswd judgeapi
```

## Step 7: Configure Homework Grader Backend

On your Mac, edit `backend/.env`:

```bash
# If using SSH tunnel or direct connection
JUDGE0_MODE=self-hosted
JUDGE0_SELF_HOSTED_URL=http://YOUR_SERVER_IP:2358

# Or if using SSH tunnel:
JUDGE0_SELF_HOSTED_URL=http://localhost:2358

# Or if using nginx with domain:
JUDGE0_SELF_HOSTED_URL=http://your-domain.com
```

Restart your backend:
```bash
cd backend
python main.py
```

## Step 8: Test from Homework Grader

1. Open your homework grader: http://localhost:5173
2. Login as a student
3. Submit a solution to any problem
4. You should see real execution results!

## Troubleshooting

### Judge0 not starting

```bash
# Check logs
docker-compose logs server
docker-compose logs worker

# Common issues:
# - PostgreSQL not ready: wait 30 seconds and restart
# - Redis connection: check REDIS_PASSWORD is commented out
```

### Can't connect from Mac

```bash
# Test connection from your Mac:
curl http://YOUR_SERVER_IP:2358/about

# If connection refused:
# - Check firewall rules
# - Check Docker is running: docker ps
# - Check port binding: netstat -tlnp | grep 2358
```

### Submissions timing out

```bash
# Increase timeout in judge0.conf:
CPU_TIME_LIMIT=10
WALL_TIME_LIMIT=20

# Restart Judge0
docker-compose restart
```

### "No such file or directory" errors

This means isolate sandbox isn't working. On Linux (not Mac), this should work fine. If you still see it:

```bash
# Check if isolate is working:
docker exec judge0-worker-1 isolate --init
docker exec judge0-worker-1 ls -la /var/local/lib/isolate/

# Should show sandbox directory
```

## Performance Tips

### For Production Use:

1. **Use PostgreSQL persistently**: The docker-compose already has volume mounts

2. **Increase worker count** in `judge0.conf`:
   ```
   COUNT=4  # Number of parallel workers
   MAX_QUEUE_SIZE=1000
   ```

3. **Monitor resources**:
   ```bash
   docker stats
   htop
   ```

4. **Set up log rotation** (Judge0 can generate large logs)

5. **Regular backups** of PostgreSQL data:
   ```bash
   docker exec judge0-db-1 pg_dump -U judge0 judge0 > backup.sql
   ```

## Security Considerations

1. **Change default passwords** in judge0.conf
2. **Use firewall** to restrict access
3. **Keep Docker updated**: `sudo apt-get update && sudo apt-get upgrade docker-ce`
4. **Monitor for abuse**: Check logs regularly
5. **Set resource limits** in judge0.conf to prevent resource exhaustion
6. **Use HTTPS** with nginx reverse proxy for production

## Stopping/Restarting Judge0

### If using Docker Compose daemon mode:

```bash
cd ~/judge0/judge0

# Stop
docker-compose down

# Stop and remove volumes (careful - deletes all data!)
docker-compose down -v

# Restart
docker-compose restart

# View logs
docker-compose logs -f
```

### If using Screen session:

```bash
# View the Judge0 screen session
screen -r judge0

# Detach from screen (leave it running)
# Press: Ctrl+A, then D

# Stop Judge0 in screen
screen -r judge0
# Then press Ctrl+C
# Then type: docker-compose down
# Then press Ctrl+D to exit screen

# Or kill screen session entirely
screen -X -S judge0 quit
docker-compose down  # Clean up containers

# Restart Judge0 in screen
cd ~/judge0/judge0
screen -dmS judge0 bash -c "docker-compose up; exec bash"

# List all screen sessions
screen -ls
```

## Quick Reference

```bash
# Server Status
docker-compose ps

# View Logs
docker-compose logs -f server
docker-compose logs -f worker

# Restart Services
docker-compose restart server
docker-compose restart worker

# Check Judge0 Version
curl http://localhost:2358/about

# Test Submission (Hello World in C)
curl -X POST "http://localhost:2358/submissions?base64_encoded=true&wait=true" \
  -H "Content-Type: application/json" \
  -d '{"source_code":"I2luY2x1ZGUgPHN0ZGlvLmg+CgppbnQgbWFpbigpIHsKICAgIHByaW50ZigiSGVsbG8sIFdvcmxkISIpOwogICAgcmV0dXJuIDA7Cn0=","language_id":50,"stdin":""}'
```

## Next Steps for YeetCode

When you're ready to use this for YeetCode:
1. Judge0 is already set up and running
2. Just point your YeetCode backend to the same Judge0 instance
3. Consider scaling up (more workers, better server) for production
4. Add authentication if needed
5. Set up monitoring and alerting

## Support Links

- Judge0 Documentation: https://ce.judge0.com/
- Judge0 GitHub: https://github.com/judge0/judge0
- Supported Languages: https://ce.judge0.com/#system-info-languages
- Configuration Options: https://github.com/judge0/judge0/blob/master/judge0.conf
