#!/usr/bin/env python3
"""
Simple Database Monitor
======================

A simplified but functional database monitoring system for the Viejos Son Los Trapos project.
This script provides essential monitoring capabilities with emergency features.

Features:
- Database health monitoring
- Automatic cleanup
- Emergency shutdown
- Self-destruct capability
- Comprehensive logging

Usage:
    python3 db_monitor_simple.py --monitor    # Start monitoring
    python3 db_monitor_simple.py --health     # Health check
    python3 db_monitor_simple.py --cleanup    # Cleanup only
    python3 db_monitor_simple.py --emergency  # Emergency shutdown
    python3 db_monitor_simple.py --kill-self  # Self-destruct
"""

import psycopg2
import sys
import signal
import time
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# Database configuration
DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': 'viejos_trapos_db',
    'user': 'viejos_trapos_user',
    'password': 'viejos_trapos_pass'
}

class SimpleDBMonitor:
    def __init__(self):
        self.conn = None
        self.running = False
        
    def connect(self) -> bool:
        """Connect to database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = True
            print("✅ Connected to database")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        if self.conn:
            self.conn.close()
            print("🔌 Disconnected from database")
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[List]:
        """Execute a query safely"""
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in cur.fetchall()]
                return None
        except Exception as e:
            print(f"⚠️ Query failed: {e}")
            return None
    
    def get_health_metrics(self) -> Dict[str, Any]:
        """Get database health metrics"""
        metrics = {}
        
        queries = {
            'total_connections': "SELECT count(*) as count FROM pg_stat_activity",
            'active_connections': "SELECT count(*) as count FROM pg_stat_activity WHERE state != 'idle'",
            'idle_transactions': "SELECT count(*) as count FROM pg_stat_activity WHERE state = 'idle in transaction'",
            'blocked_queries': "SELECT count(*) as count FROM pg_stat_activity WHERE wait_event_type IS NOT NULL",
            'total_locks': "SELECT count(*) as count FROM pg_locks",
            'blocked_locks': "SELECT count(*) as count FROM pg_locks WHERE NOT granted"
        }
        
        for key, query in queries.items():
            result = self.execute_query(query)
            if result and len(result) > 0:
                metrics[key] = result[0]['count']
            else:
                metrics[key] = 0
        
        return metrics
    
    def check_health(self) -> Dict[str, Any]:
        """Perform comprehensive health check"""
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
            if metrics['total_connections'] > 50:
                health['alerts'].append(f"High connection count: {metrics['total_connections']}")
                health['recommendations'].append("Consider killing idle connections")
            
            if metrics['idle_transactions'] > 0:
                health['alerts'].append(f"Idle transactions: {metrics['idle_transactions']}")
                health['recommendations'].append("Kill idle transactions")
            
            if metrics['blocked_locks'] > 0:
                health['alerts'].append(f"Blocked locks: {metrics['blocked_locks']}")
                health['recommendations'].append("Kill blocking processes")
            
            if metrics['total_locks'] > 100:
                health['alerts'].append(f"High lock count: {metrics['total_locks']}")
                health['recommendations'].append("Investigate lock contention")
            
            # Determine status
            if len(health['alerts']) == 0:
                health['status'] = 'healthy'
            elif len(health['alerts']) <= 2:
                health['status'] = 'warning'
            else:
                health['status'] = 'critical'
            
            print(f"📊 Health Status: {health['status']} ({len(health['alerts'])} alerts)")
            
        except Exception as e:
            health['status'] = 'error'
            health['alerts'].append(f"Health check failed: {e}")
            print(f"❌ Health check failed: {e}")
        
        return health
    
    def kill_process(self, pid: int) -> bool:
        """Kill a database process"""
        try:
            result = self.execute_query("SELECT pg_terminate_backend(%s) as result", (pid,))
            if result and len(result) > 0:
                return result[0]['result']
            return False
        except Exception as e:
            print(f"❌ Failed to kill process {pid}: {e}")
            return False
    
    def cleanup_problematic_processes(self) -> Dict[str, int]:
        """Clean up problematic processes"""
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
                    print(f"🔪 Killed idle transaction {proc['pid']}")
            
            # Kill long running processes (> 5 minutes)
            long_running_query = """
            SELECT pid, usename, state, query_start
            FROM pg_stat_activity 
            WHERE state != 'idle'
            AND query_start < now() - interval '5 minutes'
            AND pid != pg_backend_pid()
            """
            
            long_running = self.execute_query(long_running_query) or []
            for proc in long_running:
                if self.kill_process(proc['pid']):
                    results['long_running_killed'] += 1
                    print(f"🔪 Killed long running process {proc['pid']}")
            
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
                    print(f"🔪 Killed blocking process {proc['blocking_pid']}")
            
            total_killed = sum(results.values())
            if total_killed > 0:
                print(f"✅ Cleanup completed: {total_killed} processes killed")
            else:
                print("✅ No problematic processes found")
            
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
        
        return results
    
    def emergency_shutdown(self):
        """Emergency shutdown - kill all non-essential processes"""
        print("🚨 EMERGENCY SHUTDOWN INITIATED!")
        
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
                    print(f"🚨 EMERGENCY: Killed process {proc['pid']} ({proc['application_name']})")
            
            print(f"🚨 EMERGENCY SHUTDOWN COMPLETED: {killed_count} processes killed")
            
        except Exception as e:
            print(f"❌ Emergency shutdown failed: {e}")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        print("🔄 Starting monitoring loop...")
        
        while self.running:
            try:
                # Get health status
                health = self.check_health()
                
                # Perform cleanup if needed
                if health['status'] in ['warning', 'critical']:
                    print("🧹 Performing cleanup...")
                    cleanup_results = self.cleanup_problematic_processes()
                    if sum(cleanup_results.values()) > 0:
                        print(f"📊 Cleanup results: {cleanup_results}")
                
                # Wait before next check
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"❌ Monitoring loop error: {e}")
                time.sleep(30)
    
    def start_monitoring(self):
        """Start the monitoring system"""
        if not self.connect():
            return
        
        self.running = True
        
        try:
            self.monitor_loop()
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        finally:
            self.disconnect()

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print(f"\n🛑 Received signal {signum}, shutting down...")
    sys.exit(0)

def main():
    """Main entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if len(sys.argv) < 2:
        print("Usage: python3 db_monitor_simple.py [--monitor|--health|--cleanup|--emergency|--kill-self]")
        sys.exit(1)
    
    monitor = SimpleDBMonitor()
    
    try:
        if sys.argv[1] == '--monitor':
            monitor.start_monitoring()
        elif sys.argv[1] == '--health':
            if monitor.connect():
                health = monitor.check_health()
                print(json.dumps(health, indent=2))
                monitor.disconnect()
        elif sys.argv[1] == '--cleanup':
            if monitor.connect():
                results = monitor.cleanup_problematic_processes()
                print(json.dumps(results, indent=2))
                monitor.disconnect()
        elif sys.argv[1] == '--emergency':
            if monitor.connect():
                monitor.emergency_shutdown()
                monitor.disconnect()
        elif sys.argv[1] == '--kill-self':
            print("💥 SELF-DESTRUCT INITIATED!")
            os.kill(os.getpid(), signal.SIGTERM)
        else:
            print("Unknown option. Use --monitor, --health, --cleanup, --emergency, or --kill-self")
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 