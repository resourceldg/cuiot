#!/bin/bash
"""
Automated Database Monitoring Script
===================================

This script provides easy-to-use automation for database monitoring.
It's designed to be simple, efficient, and production-ready.

Features:
- One-command setup
- Automatic health monitoring
- Emergency procedures
- Log management
- Status reporting

Usage:
    ./auto_monitor.sh [COMMAND]

Commands:
    setup       - Install and configure monitoring
    start       - Start monitoring daemon
    stop        - Stop monitoring daemon
    status      - Check monitoring status
    health      - Perform health check
    cleanup     - Perform cleanup
    emergency   - Emergency shutdown
    destroy     - Self-destruct monitoring
    logs        - Show recent logs
    help        - Show this help

Examples:
    # Quick setup and start
    ./auto_monitor.sh setup && ./auto_monitor.sh start
    
    # Check health
    ./auto_monitor.sh health
    
    # Emergency shutdown
    ./auto_monitor.sh emergency
    
    # View status
    ./auto_monitor.sh status

AUTHOR: AI Assistant
VERSION: 1.0.0
"""

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/db_monitor_simple.py"
PID_FILE="/tmp/db_monitor.pid"
LOG_FILE="/tmp/db_monitor.log"
LOCK_FILE="/tmp/db_monitor.lock"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
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

# Check if running in Docker
check_docker() {
    if [[ -f /.dockerenv ]] || grep -q docker /proc/1/cgroup 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Check if monitor script exists
check_monitor_script() {
    if [[ ! -f "$MONITOR_SCRIPT" ]]; then
        log_error "Monitor script not found: $MONITOR_SCRIPT"
        exit 1
    fi
}

# Create log file
create_log_file() {
    touch "$LOG_FILE"
    chmod 644 "$LOG_FILE"
    log_info "Log file created: $LOG_FILE"
}

# Check if monitoring is running
is_running() {
    if [[ -f "$PID_FILE" ]]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up database monitoring..."
    
    check_monitor_script
    create_log_file
    
    # Make script executable
    chmod +x "$MONITOR_SCRIPT"
    
    # Create PID directory
    mkdir -p "$(dirname "$PID_FILE")"
    
    log_info "Monitoring setup completed"
}

# Start monitoring
start_monitoring() {
    log_info "Starting database monitoring..."
    
    if is_running; then
        log_warn "Monitoring is already running"
        return
    fi
    
    # Start monitoring in background
    nohup python3 "$MONITOR_SCRIPT" --monitor > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    
    # Wait a moment and check if it started
    sleep 2
    if is_running; then
        log_info "Monitoring started successfully (PID: $(cat "$PID_FILE"))"
    else
        log_error "Failed to start monitoring"
        exit 1
    fi
}

# Stop monitoring
stop_monitoring() {
    log_info "Stopping database monitoring..."
    
    if is_running; then
        PID=$(cat "$PID_FILE")
        kill "$PID"
        
        # Wait for graceful shutdown
        for i in {1..10}; do
            if ! kill -0 "$PID" 2>/dev/null; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if kill -0 "$PID" 2>/dev/null; then
            log_warn "Force killing monitoring process"
            kill -9 "$PID"
        fi
        
        rm -f "$PID_FILE"
        log_info "Monitoring stopped"
    else
        log_warn "Monitoring is not running"
    fi
}

# Check status
check_status() {
    log_info "Checking monitoring status..."
    
    echo "=== Database Monitoring Status ==="
    
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo -e "Status: ${GREEN}RUNNING${NC}"
        echo "PID: $PID"
        echo "Uptime: $(ps -o etime= -p "$PID" 2>/dev/null || echo 'Unknown')"
    else
        echo -e "Status: ${RED}STOPPED${NC}"
    fi
    
    if [[ -f "$LOG_FILE" ]]; then
        echo -e "Log File: ${GREEN}EXISTS${NC}"
        echo "Log Size: $(du -h "$LOG_FILE" | cut -f1)"
        echo "Log Lines: $(wc -l < "$LOG_FILE")"
    else
        echo -e "Log File: ${RED}MISSING${NC}"
    fi
    
    echo "================================"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    if check_docker; then
        # Running in Docker container
        python3 "$MONITOR_SCRIPT" --health
    else
        # Running on host
        docker exec viejos_trapos_backend python3 /app/scripts/db_monitor_simple.py --health
    fi
}

# Cleanup
cleanup() {
    log_info "Performing cleanup..."
    
    if check_docker; then
        # Running in Docker container
        python3 "$MONITOR_SCRIPT" --cleanup
    else
        # Running on host
        docker exec viejos_trapos_backend python3 /app/scripts/db_monitor_simple.py --cleanup
    fi
}

# Emergency shutdown
emergency_shutdown() {
    log_error "🚨 EMERGENCY SHUTDOWN INITIATED!"
    
    # Stop monitoring
    stop_monitoring
    
    # Run emergency shutdown
    if check_docker; then
        python3 "$MONITOR_SCRIPT" --emergency
    else
        docker exec viejos_trapos_backend python3 /app/scripts/db_monitor_simple.py --emergency
    fi
    
    log_error "🚨 Emergency shutdown completed"
}

# Self-destruct
self_destruct() {
    log_error "💥 SELF-DESTRUCT INITIATED!"
    
    # Stop monitoring
    stop_monitoring
    
    # Run self-destruct
    if check_docker; then
        python3 "$MONITOR_SCRIPT" --kill-self
    else
        docker exec viejos_trapos_backend python3 /app/scripts/db_monitor_simple.py --kill-self
    fi
    
    # Clean up files
    rm -f "$PID_FILE" "$LOG_FILE" "$LOCK_FILE"
    
    log_error "💥 Self-destruct completed"
}

# Show logs
show_logs() {
    log_info "Showing recent logs..."
    
    if [[ -f "$LOG_FILE" ]]; then
        echo "=== Recent Database Monitor Logs ==="
        tail -n 50 "$LOG_FILE"
        echo "==================================="
    else
        log_error "Log file not found: $LOG_FILE"
    fi
}

# Show help
show_help() {
    echo "Automated Database Monitoring Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup       - Install and configure monitoring"
    echo "  start       - Start monitoring daemon"
    echo "  stop        - Stop monitoring daemon"
    echo "  status      - Check monitoring status"
    echo "  health      - Perform health check"
    echo "  cleanup     - Perform cleanup"
    echo "  emergency   - Emergency shutdown"
    echo "  destroy     - Self-destruct monitoring"
    echo "  logs        - Show recent logs"
    echo "  help        - Show this help"
    echo ""
    echo "Examples:"
    echo "  # Quick setup and start"
    echo "  $0 setup && $0 start"
    echo ""
    echo "  # Check health"
    echo "  $0 health"
    echo ""
    echo "  # Emergency shutdown"
    echo "  $0 emergency"
    echo ""
    echo "  # View status"
    echo "  $0 status"
}

# Main function
main() {
    case "${1:-}" in
        setup)
            setup_monitoring
            ;;
        start)
            start_monitoring
            ;;
        stop)
            stop_monitoring
            ;;
        status)
            check_status
            ;;
        health)
            health_check
            ;;
        cleanup)
            cleanup
            ;;
        emergency)
            emergency_shutdown
            ;;
        destroy)
            self_destruct
            ;;
        logs)
            show_logs
            ;;
        help|--help|-h|"")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            echo "Use '$0 help' for usage information"
            exit 1
            ;;
    esac
}

# Run main function
main "$@" 