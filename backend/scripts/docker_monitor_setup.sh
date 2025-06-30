#!/bin/bash
"""
Docker Container Database Monitoring Setup
=========================================

This script sets up database monitoring inside Docker containers with cron jobs.

FEATURES:
- Monitoring daemon running in container
- Cron jobs inside container
- Health checks and cleanup
- Emergency procedures
- Log management

USAGE:
    ./docker_monitor_setup.sh [COMMAND]

COMMANDS:
    --install          Install monitoring in container
    --start            Start monitoring daemon
    --stop             Stop monitoring daemon
    --status           Check monitoring status
    --health           Run health check
    --cleanup          Run cleanup
    --emergency        Emergency shutdown
    --logs             Show logs
    --restart          Restart monitoring

EXAMPLES:
    # Install and start monitoring
    ./docker_monitor_setup.sh --install --start
    
    # Check status
    ./docker_monitor_setup.sh --status
    
    # Health check
    ./docker_monitor_setup.sh --health
"""

set -e

# Configuration
CONTAINER_NAME="viejos_trapos_backend"
MONITOR_SCRIPT="/app/scripts/db_monitor_simple.py"
PID_FILE="/tmp/db_monitor.pid"
LOG_FILE="/tmp/db_monitor.log"
CRON_FILE="/tmp/crontab"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${BLUE}[DEBUG]${NC} $1"
}

# Check if container is running
check_container() {
    if ! docker ps --format "table {{.Names}}" | grep -q "$CONTAINER_NAME"; then
        log_error "Container $CONTAINER_NAME is not running"
        exit 1
    fi
}

# Install monitoring in container
install_monitoring() {
    log_info "Installing database monitoring in container..."
    
    check_container
    
    # Copy monitoring script to container
    docker cp scripts/db_monitor_simple.py "$CONTAINER_NAME:$MONITOR_SCRIPT"
    
    # Make script executable
    docker exec "$CONTAINER_NAME" chmod +x "$MONITOR_SCRIPT"
    
    # Install cron in container
    docker exec "$CONTAINER_NAME" sh -c "
        # Install cron if not available
        if ! command -v crond >/dev/null 2>&1; then
            apk add --no-cache dcron
        fi
        
        # Create cron directory
        mkdir -p /var/spool/cron/crontabs
        
        # Create cron jobs
        cat > $CRON_FILE << 'EOF'
# Database Monitoring Cron Jobs
# Health check every 5 minutes
*/5 * * * * python3 $MONITOR_SCRIPT --health >> /tmp/db_monitor_health.log 2>&1

# Cleanup every 15 minutes
*/15 * * * * python3 $MONITOR_SCRIPT --cleanup >> /tmp/db_monitor_cleanup.log 2>&1

# Log rotation daily at 2 AM
0 2 * * * find /tmp -name 'db_monitor*.log' -mtime +7 -delete
EOF
        
        # Install cron jobs
        crontab $CRON_FILE
        
        # Start cron daemon
        crond -f -d 8 &
        
        echo 'Monitoring cron jobs installed'
    "
    
    log_info "Monitoring installed successfully in container"
}

# Start monitoring daemon
start_monitoring() {
    log_info "Starting monitoring daemon in container..."
    
    check_container
    
    # Check if already running
    if docker exec "$CONTAINER_NAME" test -f "$PID_FILE" 2>/dev/null; then
        PID=$(docker exec "$CONTAINER_NAME" cat "$PID_FILE" 2>/dev/null)
        if docker exec "$CONTAINER_NAME" kill -0 "$PID" 2>/dev/null; then
            log_warn "Monitoring is already running (PID: $PID)"
            return
        fi
    fi
    
    # Start monitoring daemon
    docker exec -d "$CONTAINER_NAME" python3 "$MONITOR_SCRIPT" --monitor
    
    # Wait and get PID
    sleep 2
    PID=$(docker exec "$CONTAINER_NAME" pgrep -f "db_monitor_simple.py" 2>/dev/null || echo "")
    
    if [[ -n "$PID" ]]; then
        docker exec "$CONTAINER_NAME" sh -c "echo $PID > $PID_FILE"
        log_info "Monitoring daemon started (PID: $PID)"
    else
        log_error "Failed to start monitoring daemon"
        exit 1
    fi
}

# Stop monitoring daemon
stop_monitoring() {
    log_info "Stopping monitoring daemon in container..."
    
    check_container
    
    if docker exec "$CONTAINER_NAME" test -f "$PID_FILE" 2>/dev/null; then
        PID=$(docker exec "$CONTAINER_NAME" cat "$PID_FILE" 2>/dev/null)
        if docker exec "$CONTAINER_NAME" kill -0 "$PID" 2>/dev/null; then
            docker exec "$CONTAINER_NAME" kill "$PID"
            log_info "Monitoring daemon stopped (PID: $PID)"
        fi
        docker exec "$CONTAINER_NAME" rm -f "$PID_FILE"
    else
        # Kill any remaining monitoring processes
        docker exec "$CONTAINER_NAME" pkill -f "db_monitor_simple.py" 2>/dev/null || true
        log_info "All monitoring processes stopped"
    fi
}

# Check monitoring status
check_status() {
    log_info "Checking monitoring status in container..."
    
    check_container
    
    echo "=== Database Monitoring Status (Container) ==="
    
    # Check daemon
    if docker exec "$CONTAINER_NAME" test -f "$PID_FILE" 2>/dev/null; then
        PID=$(docker exec "$CONTAINER_NAME" cat "$PID_FILE" 2>/dev/null)
        if docker exec "$CONTAINER_NAME" kill -0 "$PID" 2>/dev/null; then
            echo -e "Daemon Status: ${GREEN}RUNNING${NC} (PID: $PID)"
        else
            echo -e "Daemon Status: ${RED}DEAD${NC} (PID: $PID)"
        fi
    else
        echo -e "Daemon Status: ${RED}STOPPED${NC}"
    fi
    
    # Check cron jobs
    if docker exec "$CONTAINER_NAME" crontab -l 2>/dev/null | grep -q "db_monitor"; then
        echo -e "Cron Jobs: ${GREEN}INSTALLED${NC}"
        echo "Active cron jobs:"
        docker exec "$CONTAINER_NAME" crontab -l | grep "db_monitor"
    else
        echo -e "Cron Jobs: ${RED}NOT INSTALLED${NC}"
    fi
    
    # Check log files
    if docker exec "$CONTAINER_NAME" test -f "/tmp/db_monitor_health.log" 2>/dev/null; then
        LINES=$(docker exec "$CONTAINER_NAME" wc -l < /tmp/db_monitor_health.log)
        echo -e "Health Log: ${GREEN}EXISTS${NC} ($LINES lines)"
    else
        echo -e "Health Log: ${RED}MISSING${NC}"
    fi
    
    if docker exec "$CONTAINER_NAME" test -f "/tmp/db_monitor_cleanup.log" 2>/dev/null; then
        LINES=$(docker exec "$CONTAINER_NAME" wc -l < /tmp/db_monitor_cleanup.log)
        echo -e "Cleanup Log: ${GREEN}EXISTS${NC} ($LINES lines)"
    else
        echo -e "Cleanup Log: ${RED}MISSING${NC}"
    fi
    
    echo "============================================="
}

# Run health check
health_check() {
    log_info "Running health check in container..."
    
    check_container
    
    docker exec "$CONTAINER_NAME" python3 "$MONITOR_SCRIPT" --health
}

# Run cleanup
cleanup() {
    log_info "Running cleanup in container..."
    
    check_container
    
    docker exec "$CONTAINER_NAME" python3 "$MONITOR_SCRIPT" --cleanup
}

# Emergency shutdown
emergency_shutdown() {
    log_error "🚨 EMERGENCY SHUTDOWN INITIATED!"
    
    check_container
    
    # Stop monitoring
    stop_monitoring
    
    # Run emergency shutdown
    docker exec "$CONTAINER_NAME" python3 "$MONITOR_SCRIPT" --emergency
    
    log_error "🚨 Emergency shutdown completed"
}

# Show logs
show_logs() {
    log_info "Showing logs from container..."
    
    check_container
    
    echo "=== Recent Health Check Logs ==="
    docker exec "$CONTAINER_NAME" tail -n 20 /tmp/db_monitor_health.log 2>/dev/null || echo "No health logs found"
    
    echo ""
    echo "=== Recent Cleanup Logs ==="
    docker exec "$CONTAINER_NAME" tail -n 20 /tmp/db_monitor_cleanup.log 2>/dev/null || echo "No cleanup logs found"
    
    echo ""
    echo "=== Recent Monitoring Logs ==="
    docker exec "$CONTAINER_NAME" tail -n 20 /tmp/db_monitor.log 2>/dev/null || echo "No monitoring logs found"
}

# Restart monitoring
restart_monitoring() {
    log_info "Restarting monitoring in container..."
    
    stop_monitoring
    sleep 2
    start_monitoring
    
    log_info "Monitoring restarted"
}

# Show help
show_help() {
    echo "Docker Container Database Monitoring Setup"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "COMMANDS:"
    echo "  --install          Install monitoring in container"
    echo "  --start            Start monitoring daemon"
    echo "  --stop             Stop monitoring daemon"
    echo "  --status           Check monitoring status"
    echo "  --health           Run health check"
    echo "  --cleanup          Run cleanup"
    echo "  --emergency        Emergency shutdown"
    echo "  --logs             Show logs"
    echo "  --restart          Restart monitoring"
    echo "  --help             Show this help"
    echo ""
    echo "EXAMPLES:"
    echo "  # Install and start monitoring"
    echo "  $0 --install && $0 --start"
    echo ""
    echo "  # Check status"
    echo "  $0 --status"
    echo ""
    echo "  # Health check"
    echo "  $0 --health"
}

# Main function
main() {
    case "${1:-}" in
        --install)
            install_monitoring
            ;;
        --start)
            start_monitoring
            ;;
        --stop)
            stop_monitoring
            ;;
        --status)
            check_status
            ;;
        --health)
            health_check
            ;;
        --cleanup)
            cleanup
            ;;
        --emergency)
            emergency_shutdown
            ;;
        --logs)
            show_logs
            ;;
        --restart)
            restart_monitoring
            ;;
        --help|-h|"")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 