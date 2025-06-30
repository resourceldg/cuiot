# Database Monitoring System Documentation

## Overview

The Database Monitoring System is a production-ready solution designed to monitor, maintain, and protect PostgreSQL databases in both development and production environments. It provides real-time health monitoring, automatic cleanup, emergency shutdown capabilities, and comprehensive logging.

## Features

### 🔍 **Real-time Monitoring**
- Continuous database health monitoring
- Configurable monitoring intervals
- Automatic threshold detection
- Real-time alerting

### 🧹 **Automatic Cleanup**
- Idle transaction cleanup
- Long-running query termination
- Blocking process resolution
- Lock contention resolution

### 🚨 **Emergency Capabilities**
- Emergency shutdown (kills all non-essential processes)
- Self-destruct mechanism (kills monitoring process itself)
- Signal-based emergency triggers
- Graceful shutdown handling

### 📊 **Comprehensive Logging**
- Structured logging with multiple levels
- File and console output
- Log rotation and cleanup
- Performance metrics tracking

### ⚙️ **Production-Safe Operations**
- Timeout protection for all operations
- Connection pooling awareness
- Non-blocking operations
- Resource cleanup

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Systemd       │    │   Cron Jobs     │    │   Monitoring    │
│   Service       │    │                 │    │   Script        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   Database      │
                    └─────────────────┘
```

## Installation

### Quick Setup

```bash
# Install and start monitoring system
sudo ./scripts/setup_db_monitoring.sh --install --start

# Check status
./scripts/setup_db_monitoring.sh --status
```

### Manual Installation

1. **Copy monitoring script:**
   ```bash
   cp scripts/db_monitor_production_ready.py /usr/local/bin/
   chmod +x /usr/local/bin/db_monitor_production_ready.py
   ```

2. **Create log directory:**
   ```bash
   sudo mkdir -p /var/log
   sudo touch /var/log/db_monitor.log
   sudo chmod 644 /var/log/db_monitor.log
   ```

3. **Create PID directory:**
   ```bash
   sudo mkdir -p /var/run
   ```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `postgres` | Database host |
| `DB_PORT` | `5432` | Database port |
| `DB_NAME` | `viejos_trapos_db` | Database name |
| `DB_USER` | `viejos_trapos_user` | Database user |
| `DB_PASSWORD` | `viejos_trapos_pass` | Database password |
| `DB_MONITOR_INTERVAL` | `300` | Monitoring interval (seconds) |
| `DB_MONITOR_TIMEOUT` | `30` | Query timeout (seconds) |
| `DB_MONITOR_MAX_CONNECTIONS` | `50` | Max connections threshold |
| `DB_MONITOR_MAX_LOCKS` | `100` | Max locks threshold |
| `DB_MONITOR_LOG_LEVEL` | `INFO` | Log level |
| `DB_MONITOR_LOG_FILE` | `/var/log/db_monitor.log` | Log file path |
| `DB_MONITOR_PID_FILE` | `/var/run/db_monitor.pid` | PID file path |

### Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Total Connections | 30 | 50 | Kill idle connections |
| Total Locks | 50 | 100 | Investigate lock contention |
| Blocked Locks | 1 | 5 | Kill blocking processes |
| Idle Transactions | 1 | 3 | Kill idle transactions |
| Long Running Queries | 1 | 5 | Kill long queries |

## Usage

### Basic Commands

```bash
# Start continuous monitoring
python3 scripts/db_monitor_production_ready.py --monitor

# One-time health check
python3 scripts/db_monitor_production_ready.py --health-check

# Perform cleanup
python3 scripts/db_monitor_production_ready.py --cleanup

# Emergency shutdown
python3 scripts/db_monitor_production_ready.py --emergency-shutdown

# Self-destruct
python3 scripts/db_monitor_production_ready.py --self-destruct
```

### Setup Script Commands

```bash
# Install monitoring system
sudo ./scripts/setup_db_monitoring.sh --install

# Start monitoring
sudo ./scripts/setup_db_monitoring.sh --start

# Check status
./scripts/setup_db_monitoring.sh --status

# Stop monitoring
sudo ./scripts/setup_db_monitoring.sh --stop

# Emergency shutdown
sudo ./scripts/setup_db_monitoring.sh --emergency

# Self-destruct
sudo ./scripts/setup_db_monitoring.sh --self-destruct

# View logs
./scripts/setup_db_monitoring.sh --logs

# Show configuration
./scripts/setup_db_monitoring.sh --config
```

## Monitoring Modes

### 1. **Continuous Monitoring**
- Runs as a daemon process
- Monitors database health at regular intervals
- Automatically performs cleanup when needed
- Logs all activities

### 2. **Health Check Mode**
- Performs one-time health assessment
- Returns JSON-formatted results
- No automatic actions taken
- Suitable for integration with monitoring systems

### 3. **Cleanup Mode**
- Performs cleanup operations only
- Kills problematic processes
- Resolves lock contention
- Reports cleanup results

### 4. **Emergency Mode**
- Kills all non-essential database processes
- Used in critical situations
- Immediate response to database issues
- Should be used with caution

## Emergency Procedures

### 🚨 **Emergency Shutdown**

When the database is in a critical state:

```bash
# Emergency shutdown
sudo ./scripts/setup_db_monitoring.sh --emergency

# Or directly
python3 scripts/db_monitor_production_ready.py --emergency-shutdown
```

**What it does:**
- Kills all non-essential database processes
- Terminates idle transactions
- Resolves lock contention
- Logs all actions

### 💥 **Self-Destruct**

When the monitoring system itself is causing problems:

```bash
# Self-destruct
sudo ./scripts/setup_db_monitoring.sh --self-destruct

# Or directly
python3 scripts/db_monitor_production_ready.py --self-destruct
```

**What it does:**
- Kills the monitoring process itself
- Removes PID file
- Cleans up monitoring artifacts
- Stops all monitoring activities

### 📞 **Signal-Based Emergency**

Send signals to the monitoring process:

```bash
# Emergency shutdown signal
sudo kill -USR1 $(cat /var/run/db_monitor.pid)

# Graceful shutdown signal
sudo kill -TERM $(cat /var/run/db_monitor.pid)
```

## Logging

### Log Levels

- **DEBUG**: Detailed debugging information
- **INFO**: General information about operations
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for actual problems

### Log Format

```
2024-01-15 10:30:45 - DBMonitor - INFO - Database health: healthy - 0 alerts
2024-01-15 10:30:45 - DBMonitor - WARNING - High connection count: 45
2024-01-15 10:30:45 - DBMonitor - ERROR - Failed to kill process 12345: permission denied
```

### Log Management

```bash
# View recent logs
tail -f /var/log/db_monitor.log

# Search for errors
grep ERROR /var/log/db_monitor.log

# View logs for specific date
grep "2024-01-15" /var/log/db_monitor.log
```

## Integration

### Systemd Integration

The monitoring system integrates with systemd for automatic startup:

```bash
# Enable automatic startup
sudo systemctl enable db-monitor.service

# Check service status
sudo systemctl status db-monitor.service

# View service logs
sudo journalctl -u db-monitor.service -f
```

### Cron Integration

Automated tasks run via cron:

```bash
# Health check every 5 minutes
*/5 * * * * root /usr/bin/python3 /path/to/db_monitor_production_ready.py --health-check

# Cleanup every 15 minutes
*/15 * * * * root /usr/bin/python3 /path/to/db_monitor_production_ready.py --cleanup
```

### Monitoring System Integration

Integrate with external monitoring systems:

```bash
# Health check for Nagios
python3 scripts/db_monitor_production_ready.py --health-check | grep -q "healthy" && echo "OK" || echo "CRITICAL"

# Metrics for Prometheus
python3 scripts/db_monitor_production_ready.py --health-check | jq '.metrics'
```

## Troubleshooting

### Common Issues

#### 1. **Connection Refused**
```
❌ Failed to connect to database: connection refused
```

**Solution:**
- Check if PostgreSQL is running
- Verify database credentials
- Check network connectivity

#### 2. **Permission Denied**
```
❌ Failed to kill process 12345: permission denied
```

**Solution:**
- Run as root or database superuser
- Check database user permissions
- Verify process ownership

#### 3. **Timeout Errors**
```
⚠️ Query timed out after 30 seconds
```

**Solution:**
- Increase timeout value
- Check database performance
- Investigate slow queries

#### 4. **PID File Issues**
```
⚠️ Could not write PID file: permission denied
```

**Solution:**
- Check directory permissions
- Ensure proper ownership
- Verify disk space

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# Set debug level
export DB_MONITOR_LOG_LEVEL=DEBUG

# Run with verbose output
python3 scripts/db_monitor_production_ready.py --monitor --verbose
```

### Health Check Analysis

Analyze health check results:

```bash
# Get detailed health report
python3 scripts/db_monitor_production_ready.py --health-check | jq '.'

# Check specific metrics
python3 scripts/db_monitor_production_ready.py --health-check | jq '.metrics.total_connections'
```

## Security Considerations

### 1. **Database Credentials**
- Store credentials securely
- Use environment variables
- Rotate passwords regularly
- Limit database user permissions

### 2. **Process Management**
- Monitor process permissions
- Validate PID files
- Secure log files
- Protect configuration files

### 3. **Network Security**
- Use encrypted connections
- Restrict network access
- Monitor connection attempts
- Implement firewall rules

### 4. **Audit Trail**
- Log all administrative actions
- Monitor for suspicious activity
- Regular security reviews
- Compliance reporting

## Performance Impact

### Monitoring Overhead
- **CPU**: < 1% during normal operation
- **Memory**: ~10MB for monitoring process
- **Network**: Minimal database queries
- **Disk**: Log file growth (~1MB/day)

### Optimization Tips
- Adjust monitoring intervals based on load
- Use appropriate log levels
- Implement log rotation
- Monitor monitoring system performance

## Best Practices

### 1. **Installation**
- Install in dedicated environment
- Use proper permissions
- Test in staging first
- Document configuration

### 2. **Configuration**
- Set appropriate thresholds
- Use environment variables
- Regular configuration reviews
- Version control configuration

### 3. **Monitoring**
- Regular health checks
- Monitor monitoring system
- Set up alerting
- Document procedures

### 4. **Maintenance**
- Regular log cleanup
- Update monitoring scripts
- Review and adjust thresholds
- Test emergency procedures

## Support and Maintenance

### Regular Tasks
- [ ] Daily health check review
- [ ] Weekly log analysis
- [ ] Monthly threshold review
- [ ] Quarterly security audit

### Emergency Contacts
- Database Administrator
- System Administrator
- DevOps Team
- Security Team

### Documentation Updates
- Update this documentation regularly
- Document any configuration changes
- Record incident responses
- Maintain runbooks

## License

This monitoring system is licensed under the MIT License. See LICENSE file for details.

## Contributing

To contribute to this monitoring system:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Version History

- **v1.0.0**: Initial release with basic monitoring
- **v1.1.0**: Added emergency shutdown capabilities
- **v1.2.0**: Enhanced logging and reporting
- **v1.3.0**: Production-ready features

---

**Note**: This monitoring system is designed for production use but should be thoroughly tested in your specific environment before deployment. 