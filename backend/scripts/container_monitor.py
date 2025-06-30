#!/usr/bin/env python3
"""
Container Database Monitor
=========================

Continuous database monitoring script designed to run inside Docker containers.
This script provides automated monitoring without requiring cron.

FEATURES:
- Continuous health monitoring
- Automatic cleanup
- Emergency procedures
- Log management
- Configurable intervals

USAGE:
    python3 container_monitor.py [OPTIONS]

OPTIONS:
    --monitor          Start continuous monitoring
    --health           Run health check
    --cleanup          Run cleanup
    --emergency        Emergency shutdown
    --config           Show configuration

EXAMPLES:
    # Start continuous monitoring
    python3 container_monitor.py --monitor
    
    # Health check
    python3 container_monitor.py --health
    
    # Cleanup
    python3 container_monitor.py --cleanup
"""

import argparse
import psycopg2
import sys
import signal
import time
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import threading

# Database configuration
DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': 'viejos_trapos_db',
    'user': 'viejos_trapos_user',
    'password': 'viejos_trapos_pass'
}

# Monitoring configuration
MONITOR_CONFIG = {
    'health_interval': 300,  # 5 minutes
    'cleanup_interval': 900,  # 15 minutes
    'timeout': 30,
    'max_connections': 50,
    'max_locks': 100,
    'max_idle_time': 600,  # 10 minutes
    'max_long_running': 300,  # 5 minutes
    'log_file': '/tmp/container_monitor.log'
}

class ContainerDatabaseMonitor:
    """Container-based database monitoring system."""
    
    def __init__(self, config: Dict[str, Any], monitor_config: Dict[str, Any]):
        self.config = config
        self.monitor_config = monitor_config
        self.conn = None
        self.running = False
        self.monitor_thread = None
        
        # Setup logging
        self.setup_logging()
        
        # Setup signal handlers
        self.setup_signal_handlers()
    
    def setup_logging(self):
        """Setup logging system."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.monitor_config['log_file']),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('ContainerMonitor')
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop_monitoring()
        sys.exit(0)
    
    def connect(self) -> bool:
        """Establish database connection."""
        try:
            config_with_timeout = self.config.copy()
            config_with_timeout['connect_timeout'] = 10
            
            self.conn = psycopg2.connect(**config_with_timeout)
            self.conn.autocommit = True
            
            # Set statement timeout
            with self.conn.cursor() as cur:
                cur.execute(f"SET statement_timeout = {self.monitor_config['timeout'] * 1000}")
            
            self.logger.info("✅ Connected to database successfully")
            return True
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self.conn:
            try:
                self.conn.close()
                self.logger.info("🔌 Database connection closed")
            except:
                pass
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[List]:
        """Execute a query safely."""
        if not self.conn:
            return None
            
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in cur.fetchall()]
                return None
        except Exception as e:
            self.logger.warning(f"⚠️ Query failed: {e}")
            return None
    
    def get_health_metrics(self) -> Dict[str, Any]:
        """Get database health metrics."""
        metrics = {}
        
        queries = {
            'total_connections': "SELECT count(*) as count FROM pg_stat_activity",
            'active_connections': "SELECT count(*) as count FROM pg_stat_activity WHERE state != 'idle'",
            'idle_transactions': "SELECT count(*) as count FROM pg_stat_activity WHERE state = 'idle in transaction'",
            'blocked_queries': "SELECT count(*) as count FROM pg_stat_activity WHERE wait_event_type IS NOT NULL",
            'total_locks': "SELECT count(*) as count FROM pg_locks",
            'blocked_locks': "SELECT count(*) as count FROM pg_locks WHERE NOT granted",
            'long_running_queries': f"SELECT count(*) as count FROM pg_stat_activity WHERE state != 'idle' AND query_start < now() - interval '{self.monitor_config['max_long_running']} seconds'"
        }
        
        for key, query in queries.items():
            result = self.execute_query(query)
            if result and len(result) > 0:
                metrics[key] = result[0]['count']
            else:
                metrics[key] = 0
        
        return metrics
    
    def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check."""
        health = {
            'timestamp': datetime.now().isoformat(),
            'status': 'unknown',
            'metrics': {},
            'alerts': [],
            'recommendations': []
        }
        
        try:
            health['metrics'] = self.get_health_metrics()
            metrics = health['metrics']
            
            # Check for issues
            if metrics['total_connections'] > self.monitor_config['max_connections']:
                health['alerts'].append(f"High connection count: {metrics['total_connections']}")
                health['recommendations'].append("Consider killing idle connections")
            
            if metrics['idle_transactions'] > 0:
                health['alerts'].append(f"Idle transactions: {metrics['idle_transactions']}")
                health['recommendations'].append("Kill idle transactions")
            
            if metrics['blocked_locks'] > 0:
                health['alerts'].append(f"Blocked locks: {metrics['blocked_locks']}")
                health['recommendations'].append("Kill blocking processes")
            
            if metrics['total_locks'] > self.monitor_config['max_locks']:
                health['alerts'].append(f"High lock count: {metrics['total_locks']}")
                health['recommendations'].append("Investigate lock contention")
            
            # Determine status
            if len(health['alerts']) == 0:
                health['status'] = 'healthy'
            elif len(health['alerts']) <= 2:
                health['status'] = 'warning'
            else:
                health['status'] = 'critical'
            
            self.logger.info(f"📊 Health Status: {health['status']} ({len(health['alerts'])} alerts)")
            
        except Exception as e:
            health['status'] = 'error'
            health['alerts'].append(f"Health check failed: {e}")
            self.logger.error(f"Health check failed: {e}")
        
        return health
    
    def kill_process(self, pid: int) -> bool:
        """Kill a database process."""
        try:
            result = self.execute_query("SELECT pg_terminate_backend(%s) as result", (pid,))
            if result and len(result) > 0:
                return result[0]['result']
            return False
        except Exception as e:
            self.logger.error(f"Failed to kill process {pid}: {e}")
            return False
    
    def cleanup_problematic_processes(self) -> Dict[str, int]:
        """Clean up problematic processes."""
        results = {
            'idle_transactions_killed': 0,
            'long_running_killed': 0,
            'blocking_processes_killed': 0
        }
        
        try:
            # Kill idle transactions
            idle_query = """
            SELECT pid, usename, state
            FROM pg_stat_activity 
            WHERE state = 'idle in transaction'
            AND pid != pg_backend_pid()
            """
            
            idle_processes = self.execute_query(idle_query) or []
            for proc in idle_processes:
                if self.kill_process(proc['pid']):
                    results['idle_transactions_killed'] += 1
                    self.logger.info(f"🔪 Killed idle transaction {proc['pid']}")
            
            # Kill long running processes
            long_running_query = f"""
            SELECT 
                pid,
                usename,
                state,
                query_start,
                EXTRACT(EPOCH FROM (now() - query_start))/60 as duration_minutes
            FROM pg_stat_activity 
            WHERE state != 'idle'
            AND query_start < now() - interval '{self.monitor_config['max_long_running']} seconds'
            AND pid != pg_backend_pid()
            """
            
            long_running = self.execute_query(long_running_query) or []
            for proc in long_running:
                if self.kill_process(proc['pid']):
                    results['long_running_killed'] += 1
                    self.logger.info(f"🔪 Killed long running process {proc['pid']} (running for {proc['duration_minutes']:.1f} minutes)")
            
            # Kill blocking processes
            blocking_query = """
            SELECT DISTINCT l1.pid as blocking_pid
            FROM pg_locks l1
            JOIN pg_locks l2 ON l1.locktype = l2.locktype 
                AND l1.database = l2.database 
                AND l1.relation = l2.relation 
                AND l1.pid != l2.pid
            WHERE l1.granted = true AND l2.granted = false
            """
            
            blocking = self.execute_query(blocking_query) or []
            for proc in blocking:
                if self.kill_process(proc['blocking_pid']):
                    results['blocking_processes_killed'] += 1
                    self.logger.info(f"🔪 Killed blocking process {proc['blocking_pid']}")
            
            total_killed = sum(results.values())
            if total_killed > 0:
                self.logger.info(f"✅ Cleanup completed: {total_killed} processes killed")
            else:
                self.logger.info("✅ No problematic processes found")
            
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
        
        return results
    
    def emergency_shutdown(self):
        """Emergency shutdown - kill all non-essential processes."""
        self.logger.error("🚨 EMERGENCY SHUTDOWN INITIATED!")
        
        try:
            # Kill all non-essential processes
            kill_query = """
            SELECT pid, usename, application_name, state
            FROM pg_stat_activity 
            WHERE pid != pg_backend_pid()
            AND state != 'idle'
            AND application_name NOT IN ('postgres', 'pg_stat_statements')
            """
            
            processes = self.execute_query(kill_query) or []
            killed_count = 0
            
            for proc in processes:
                if self.kill_process(proc['pid']):
                    killed_count += 1
                    self.logger.error(f"🚨 EMERGENCY: Killed process {proc['pid']} ({proc['application_name']})")
            
            self.logger.error(f"🚨 EMERGENCY SHUTDOWN COMPLETED: {killed_count} processes killed")
            
        except Exception as e:
            self.logger.error(f"Emergency shutdown failed: {e}")
    
    def monitor_loop(self):
        """Main monitoring loop."""
        self.logger.info("🔄 Starting continuous monitoring loop...")
        
        last_health_check = 0
        last_cleanup = 0
        
        while self.running:
            try:
                current_time = time.time()
                
                # Health check every 5 minutes
                if current_time - last_health_check >= self.monitor_config['health_interval']:
                    health = self.check_health()
                    
                    if health['status'] == 'critical':
                        self.logger.error(f"CRITICAL: {len(health['alerts'])} alerts - {health['alerts']}")
                    elif health['status'] == 'warning':
                        self.logger.warning(f"WARNING: {len(health['alerts'])} alerts - {health['alerts']}")
                    else:
                        self.logger.info(f"HEALTHY: Database status normal")
                    
                    last_health_check = current_time
                
                # Cleanup every 15 minutes
                if current_time - last_cleanup >= self.monitor_config['cleanup_interval']:
                    self.logger.info("🧹 Performing scheduled cleanup...")
                    cleanup_results = self.cleanup_problematic_processes()
                    if sum(cleanup_results.values()) > 0:
                        self.logger.info(f"📊 Cleanup results: {cleanup_results}")
                    
                    last_cleanup = current_time
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
            
            # Wait before next iteration
            time.sleep(60)  # Check every minute
    
    def start_monitoring(self):
        """Start the monitoring system."""
        if self.running:
            self.logger.warning("Monitoring already running")
            return
        
        if not self.connect():
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info(f"🔄 Database monitoring started")
        self.logger.info(f"  - Health check: Every {self.monitor_config['health_interval']} seconds")
        self.logger.info(f"  - Cleanup: Every {self.monitor_config['cleanup_interval']} seconds")
        
        # Keep main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop the monitoring system."""
        self.logger.info("Stopping database monitoring...")
        self.running = False
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=10)
        
        self.disconnect()
        self.logger.info("Database monitoring stopped")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Container Database Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start continuous monitoring
  python3 container_monitor.py --monitor
  
  # Health check
  python3 container_monitor.py --health
  
  # Cleanup
  python3 container_monitor.py --cleanup
  
  # Emergency shutdown
  python3 container_monitor.py --emergency
        """
    )
    
    parser.add_argument('--monitor', action='store_true', 
                       help='Start continuous monitoring')
    parser.add_argument('--health', action='store_true',
                       help='Run health check')
    parser.add_argument('--cleanup', action='store_true',
                       help='Run cleanup')
    parser.add_argument('--emergency', action='store_true',
                       help='Emergency shutdown')
    parser.add_argument('--config', action='store_true',
                       help='Show configuration')
    
    args = parser.parse_args()
    
    # Create monitor instance
    monitor = ContainerDatabaseMonitor(DB_CONFIG, MONITOR_CONFIG)
    
    try:
        if args.emergency:
            monitor.emergency_shutdown()
        elif args.health:
            health = monitor.check_health()
            print(json.dumps(health, indent=2))
        elif args.cleanup:
            cleanup_results = monitor.cleanup_problematic_processes()
            print(json.dumps(cleanup_results, indent=2))
        elif args.monitor:
            monitor.start_monitoring()
        elif args.config:
            print("=== Container Monitor Configuration ===")
            print(f"Health Interval: {MONITOR_CONFIG['health_interval']} seconds")
            print(f"Cleanup Interval: {MONITOR_CONFIG['cleanup_interval']} seconds")
            print(f"Max Connections: {MONITOR_CONFIG['max_connections']}")
            print(f"Max Locks: {MONITOR_CONFIG['max_locks']}")
            print(f"Log File: {MONITOR_CONFIG['log_file']}")
        else:
            parser.print_help()
    
    except Exception as e:
        monitor.logger.error(f"Fatal error: {e}")
        sys.exit(1)
    
    finally:
        monitor.stop_monitoring()

if __name__ == "__main__":
    main() 