#!/bin/bash

# Database Health Check Cron Setup Script
# ======================================
# This script sets up automated database health checks using cron jobs

echo "Setting up automated database health checks..."

# Create the cron job script
cat > /tmp/db_health_cron.sh << 'EOF'
#!/bin/bash

# Database Health Check Cron Job
# Runs every 5 minutes to check and clean up database issues

# Set environment variables
export PATH=/usr/local/bin:/usr/bin:/bin
export DOCKER_COMPOSE_DIR="/home/zen/Documents/viejos_son_los_trapos"

# Log file for the cron job
LOG_FILE="/tmp/db_health_cron.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check if Docker containers are running
if ! docker ps | grep -q "viejos_trapos_backend"; then
    log_message "ERROR: Backend container is not running"
    exit 1
fi

if ! docker ps | grep -q "viejos_trapos_postgres"; then
    log_message "ERROR: PostgreSQL container is not running"
    exit 1
fi

# Run the database health check
log_message "Starting automated database health check..."
docker exec viejos_trapos_backend python3 /app/scripts/db_health_check.py --auto >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    log_message "Database health check completed successfully"
else
    log_message "ERROR: Database health check failed"
fi

# Keep only last 1000 lines of log file
tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
EOF

# Make the script executable
chmod +x /tmp/db_health_cron.sh

# Create a more frequent check for development (every 2 minutes)
cat > /tmp/db_health_dev.sh << 'EOF'
#!/bin/bash

# Development Database Health Check (more frequent)
# Runs every 2 minutes during development

export PATH=/usr/local/bin:/usr/bin:/bin
export DOCKER_COMPOSE_DIR="/home/zen/Documents/viejos_son_los_trapos"

LOG_FILE="/tmp/db_health_dev.log"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Only run if containers are up
if docker ps | grep -q "viejos_trapos_backend" && docker ps | grep -q "viejos_trapos_postgres"; then
    log_message "Running development database health check..."
    docker exec viejos_trapos_backend python3 /app/scripts/db_health_check.py --auto >> "$LOG_FILE" 2>&1
    log_message "Development check completed"
    
    # Keep only last 500 lines
    tail -n 500 "$LOG_FILE" > "$LOG_FILE.tmp" && mv "$LOG_FILE.tmp" "$LOG_FILE"
fi
EOF

chmod +x /tmp/db_health_dev.sh

# Create a manual cleanup script
cat > /tmp/manual_cleanup.sh << 'EOF'
#!/bin/bash

# Manual Database Cleanup Script
# Run this when you want to clean up the database immediately

echo "Running manual database cleanup..."

# Check if containers are running
if ! docker ps | grep -q "viejos_trapos_backend"; then
    echo "ERROR: Backend container is not running"
    exit 1
fi

if ! docker ps | grep -q "viejos_trapos_postgres"; then
    echo "ERROR: PostgreSQL container is not running"
    exit 1
fi

# Run the health check with verbose output
echo "Starting database health check and cleanup..."
docker exec -it viejos_trapos_backend python3 /app/scripts/db_health_check.py --auto --verbose

echo "Manual cleanup completed!"
EOF

chmod +x /tmp/manual_cleanup.sh

# Move scripts to a permanent location
sudo mkdir -p /usr/local/bin/db-health
sudo mv /tmp/db_health_cron.sh /usr/local/bin/db-health/
sudo mv /tmp/db_health_dev.sh /usr/local/bin/db-health/
sudo mv /tmp/manual_cleanup.sh /usr/local/bin/db-health/

echo "Scripts installed to /usr/local/bin/db-health/"

# Set up cron jobs
echo "Setting up cron jobs..."

# Add cron job for regular health checks (every 5 minutes)
(crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/db-health/db_health_cron.sh") | crontab -

# Add cron job for development (every 2 minutes, only if containers are running)
(crontab -l 2>/dev/null; echo "*/2 * * * * /usr/local/bin/db-health/db_health_dev.sh") | crontab -

echo "Cron jobs installed successfully!"

# Create aliases for easy access
echo "Creating aliases..."

# Add aliases to bashrc
cat >> ~/.bashrc << 'EOF'

# Database Health Check Aliases
alias db-cleanup='/usr/local/bin/db-health/manual_cleanup.sh'
alias db-status='docker exec viejos_trapos_backend python3 /app/scripts/db_health_check.py'
alias db-logs='tail -f /tmp/db_health_cron.log'
alias db-dev-logs='tail -f /tmp/db_health_dev.log'
EOF

echo "Aliases added to ~/.bashrc"
echo ""
echo "=== SETUP COMPLETE ==="
echo ""
echo "Available commands:"
echo "  db-cleanup    - Run manual database cleanup"
echo "  db-status     - Check database status"
echo "  db-logs       - View cron job logs"
echo "  db-dev-logs   - View development logs"
echo ""
echo "Cron jobs installed:"
echo "  - Regular health check: every 5 minutes"
echo "  - Development check: every 2 minutes"
echo ""
echo "Log files:"
echo "  - /tmp/db_health_cron.log (regular checks)"
echo "  - /tmp/db_health_dev.log (development checks)"
echo ""
echo "To reload aliases, run: source ~/.bashrc" 