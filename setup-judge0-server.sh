#!/bin/bash
# Judge0 Setup Script for Linux Server
# Run this on your remote Linux server

set -e  # Exit on error

echo "=========================================="
echo "Judge0 Setup Script"
echo "=========================================="
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "⚠️  Please run this script as a normal user (not root)"
   exit 1
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker installed"
    echo "⚠️  Please log out and back in, then run this script again"
    exit 0
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed"
fi

# Create Judge0 directory
echo ""
echo "📁 Creating Judge0 directory..."
mkdir -p ~/judge0
cd ~/judge0

# Clone Judge0 if not already present
if [ ! -d "judge0" ]; then
    echo "📥 Cloning Judge0 repository..."
    git clone https://github.com/judge0/judge0.git
else
    echo "✅ Judge0 repository already exists"
fi

cd judge0

# Create docker-compose.yml
echo ""
echo "📝 Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
x-logging:
  &default-logging
  logging:
    driver: json-file
    options:
      max-size: 100M

services:
  server:
    image: judge0/judge0:latest
    volumes:
      - ./judge0.conf:/judge0.conf:ro
    ports:
      - "2358:2358"
    privileged: true
    <<: *default-logging
    restart: always

  worker:
    image: judge0/judge0:latest
    command: ["./scripts/workers"]
    volumes:
      - ./judge0.conf:/judge0.conf:ro
    privileged: true
    <<: *default-logging
    restart: always

  db:
    image: postgres:16.2
    env_file: judge0.conf
    volumes:
      - postgres-data:/var/lib/postgresql/data/
    <<: *default-logging
    restart: always

  redis:
    image: redis:7.2.4
    command: ["redis-server", "--appendonly", "no"]
    <<: *default-logging
    restart: always

volumes:
  postgres-data:
EOF

# Download judge0.conf if not present
if [ ! -f "judge0.conf" ]; then
    echo "📥 Downloading judge0.conf..."
    wget -q https://raw.githubusercontent.com/judge0/judge0/master/judge0.conf
fi

# Modify judge0.conf to comment out REDIS_PASSWORD
echo "🔧 Configuring judge0.conf..."
sed -i 's/^REDIS_PASSWORD=$/# REDIS_PASSWORD= (commented out for local development)/' judge0.conf

# Set PostgreSQL password
if ! grep -q "POSTGRES_PASSWORD=YourPassword123" judge0.conf; then
    sed -i 's/^POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=YourPassword123/' judge0.conf
fi

# Ask user about screen vs docker-compose daemon
echo ""
echo "How would you like to run Judge0?"
echo "  1) Docker Compose daemon mode (recommended - runs in background)"
echo "  2) Screen session (keeps logs visible)"
read -p "Enter choice (1 or 2): " run_choice

if [ "$run_choice" = "2" ]; then
    # Check if screen is installed
    if ! command -v screen &> /dev/null; then
        echo "📦 Installing screen..."
        sudo apt-get update && sudo apt-get install -y screen
    fi

    echo "🚀 Starting Judge0 in screen session 'judge0'..."
    docker-compose pull

    # Start in detached screen session
    screen -dmS judge0 bash -c "docker-compose up; exec bash"

    echo ""
    echo "✅ Judge0 started in screen session"
    echo ""
    echo "Screen commands:"
    echo "  - View logs: screen -r judge0"
    echo "  - Detach from screen: Ctrl+A then D"
    echo "  - Kill screen: screen -X -S judge0 quit"
    echo ""
else
    echo "🚀 Starting Judge0 in daemon mode..."
    docker-compose pull
    docker-compose up -d
fi

echo ""
echo "⏳ Waiting for Judge0 to initialize (30 seconds)..."
sleep 30

# Test Judge0
echo ""
echo "🧪 Testing Judge0..."
if curl -s http://localhost:2358/about | grep -q "judge0"; then
    echo "✅ Judge0 is running successfully!"

    # Get server IP
    SERVER_IP=$(hostname -I | awk '{print $1}')

    echo ""
    echo "=========================================="
    echo "✅ Judge0 Setup Complete!"
    echo "=========================================="
    echo ""
    echo "Judge0 is running on:"
    echo "  - Local: http://localhost:2358"
    echo "  - Remote: http://$SERVER_IP:2358"
    echo ""
    echo "⚠️  IMPORTANT: Configure your firewall!"
    echo ""
    echo "Option 1 - SSH Tunnel (Most Secure):"
    echo "  On your Mac, run:"
    echo "  ssh -L 2358:localhost:2358 $USER@$SERVER_IP -N"
    echo ""
    echo "Option 2 - Open Firewall Port:"
    echo "  sudo ufw allow from YOUR_MAC_IP to any port 2358"
    echo ""
    echo "Next steps:"
    echo "  1. Configure firewall (see above)"
    echo "  2. Update backend/.env on your Mac:"
    echo "     JUDGE0_MODE=self-hosted"
    echo "     JUDGE0_SELF_HOSTED_URL=http://$SERVER_IP:2358"
    echo "  3. Restart your homework grader backend"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
    echo "=========================================="
else
    echo "❌ Judge0 failed to start. Check logs:"
    echo "  docker-compose logs server"
    echo "  docker-compose logs worker"
fi
EOF
chmod +x setup-judge0-server.sh
