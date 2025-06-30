#!/bin/bash
"""
Simple Database Monitoring Starter
=================================

This script starts automated database monitoring with configurable intervals.

CONFIGURATION:
- Health Check: Every 5 minutes
- Cleanup: Every 15 minutes
- Continuous Monitoring: Every 60 seconds

USAGE:
    ./start_monitoring.sh [OPTIONS]

OPTIONS:
    --start          Start all monitoring
    --stop           Stop all monitoring
    --status         Check monitoring status
    --health         Run health check now
    --cleanup        Run cleanup now

EXAMPLES:
    # Start monitoring
    ./start_monitoring.sh --start
    
    # Check status
    ./start_monitoring.sh --status
    
    # Health check
    ./start_monitoring.sh --health
"""

set -e

# Configuration
MONITOR_SCRIPT="/app/scripts/db_monitor_simple.py"
PID_FILE="/tmp/db_monitor.pid"
LOG_FILE="/tmp/db_monitor.log"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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

# Check if monitoring is running
is_running() {
    if [[ -f "$PID_FILE" ]]; then
        PID=$(cat "$PID_FILE")
        if docker exec viejos_trapos_backend kill -0 "$PID" 2>/dev/null; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# Start monitoring
start_monitoring() {
    log_info "Starting database monitoring..."
    
    if is_running; then
        log_warn "Monitoring is already running"
        return
    fi
    
    # Start continuous monitoring
    docker exec -d viejos_trapos_backend python3 "$MONITOR_SCRIPT" --monitor
    sleep 2
    
    # Get PID
    PID=$(docker exec viejos_trapos_backend pgrep -f "db_monitor_simple.py" | head -1)
    if [[ -n "$PID" ]]; then
        echo "$PID" > "$PID_FILE"
        log_info "Continuous monitoring started (PID: $PID)"
    else
        log_error "Failed to start monitoring"
        exit 1
    fi
    
    # Create cron jobs for health check and cleanup
    create_cron_jobs
    
    log_info "Monitoring system started successfully"
    log_info "  - Continuous monitoring: Every 60 seconds"
    log_info "  - Health check: Every 5 minutes"
    log_info "  - Cleanup: Every 15 minutes"
}

# Stop monitoring
stop_monitoring() {
    log_info "Stopping database monitoring..."
    
    # Stop continuous monitoring
    if is_running; then
        PID=$(cat "$PID_FILE")
        docker exec viejos_trapos_backend kill "$PID" 2>/dev/null || true
        rm -f "$PID_FILE"
        log_info "Continuous monitoring stopped"
    fi
    
    # Remove cron jobs
    remove_cron_jobs
    
    log_info "All monitoring stopped"
}

# Create cron jobs
create_cron_jobs() {
    log_info "Setting up automated cron jobs..."
    
    # Create temporary cron file
    TEMP_CRON=$(mktemp)
    
    # Add health check every 5 minutes
    echo "*/5 * * * * docker exec viejos_trapos_backend python3 $MONITOR_SCRIPT --health >> /tmp/db_monitor_health.log 2>&1" >> "$TEMP_CRON"
    
    # Add cleanup every 15 minutes
    echo "*/15 * * * * docker exec viejos_trapos_backend python3 $MONITOR_SCRIPT --cleanup >> /tmp/db_monitor_cleanup.log 2>&1" >> "$TEMP_CRON"
    
    # Install cron jobs
    crontab "$TEMP_CRON" 2>/dev/null || {
        log_warn "Could not install cron jobs (may need sudo)"
        log_info "Cron jobs created in: $TEMP_CRON"
        log_info "To install manually: crontab $TEMP_CRON"
    }
    
    rm -f "$TEMP_CRON"
}

# Remove cron jobs
remove_cron_jobs() {
    log_info "Removing cron jobs..."
    
    # Remove cron jobs containing db_monitor
    crontab -l 2>/dev/null | grep -v "db_monitor" | crontab - 2>/dev/null || true
}

# Check status
check_status() {
    log_info "Checking monitoring status..."
    
    echo "=== Database Monitoring Status ==="
    
    # Check continuous monitoring
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo -e "Continuous Monitoring: ${GREEN}RUNNING${NC} (PID: $PID)"
    else
        echo -e "Continuous Monitoring: ${RED}STOPPED${NC}"
    fi
    
    # Check cron jobs
    if crontab -l 2>/dev/null | grep -q "db_monitor"; then
        echo -e "Cron Jobs: ${GREEN}INSTALLED${NC}"
        echo "Active cron jobs:"
        crontab -l | grep "db_monitor"
    else
        echo -e "Cron Jobs: ${RED}NOT INSTALLED${NC}"
    fi
    
    # Check log files
    if [[ -f "/tmp/db_monitor_health.log" ]]; then
        echo -e "Health Log: ${GREEN}EXISTS${NC} ($(wc -l < /tmp/db_monitor_health.log) lines)"
    else
        echo -e "Health Log: ${RED}MISSING${NC}"
    fi
    
    if [[ -f "/tmp/db_monitor_cleanup.log" ]]; then
        echo -e "Cleanup Log: ${GREEN}EXISTS${NC} ($(wc -l < /tmp/db_monitor_cleanup.log) lines)"
    else
        echo -e "Cleanup Log: ${RED}MISSING${NC}"
    fi
    
    echo "================================"
}

# Run health check
health_check() {
    log_info "Running health check..."
    docker exec viejos_trapos_backend python3 "$MONITOR_SCRIPT" --health
}

# Run cleanup
cleanup() {
    log_info "Running cleanup..."
    docker exec viejos_trapos_backend python3 "$MONITOR_SCRIPT" --cleanup
}

# Show help
show_help() {
    echo "Simple Database Monitoring Starter"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "COMMANDS:"
    echo "  --start          Start all monitoring"
    echo "  --stop           Stop all monitoring"
    echo "  --status         Check monitoring status"
    echo "  --health         Run health check now"
    echo "  --cleanup        Run cleanup now"
    echo "  --help           Show this help"
    echo ""
    echo "EXAMPLES:"
    echo "  # Start monitoring"
    echo "  $0 --start"
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