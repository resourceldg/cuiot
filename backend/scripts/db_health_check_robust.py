#!/usr/bin/env python3
"""
Robust Database Health Check and Cleanup Script
==============================================

This script provides a robust database health monitoring and cleanup system
with timeouts and error handling to prevent hanging.

Features:
- Timeout protection for all database operations
- Graceful error handling
- Safe table statistics collection
- Entity-agnostic design
- Automatic cleanup capabilities
"""

import argparse
import psycopg2
import sys
import signal
from datetime import datetime, timedelta
import os
from typing import List, Dict, Any, Optional
import time

# Database connection settings
DB_CONFIG = {
    'host': 'postgres',
    'port': 5432,
    'database': 'viejos_trapos_db',
    'user': 'viejos_trapos_user',
    'password': 'viejos_trapos_pass'
}

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

class RobustDatabaseHealthChecker:
    def __init__(self, config: Dict[str, Any], timeout_seconds: int = 30):
        self.config = config
        self.conn = None
        self.timeout_seconds = timeout_seconds
        self._table_cache = None
        
    def connect(self):
        """Establish database connection with timeout"""
        try:
            # Set connection timeout
            config_with_timeout = self.config.copy()
            config_with_timeout['connect_timeout'] = 10
            
            self.conn = psycopg2.connect(**config_with_timeout)
            self.conn.autocommit = True
            
            # Set statement timeout
            with self.conn.cursor() as cur:
                cur.execute(f"SET statement_timeout = {self.timeout_seconds * 1000}")
            
            print("✅ Connected to database successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            try:
                self.conn.close()
                print("🔌 Database connection closed")
            except:
                pass
    
    def safe_execute(self, query: str, params: tuple = (), timeout: int = None) -> Optional[List]:
        """Execute query with timeout protection"""
        if timeout is None:
            timeout = self.timeout_seconds
            
        # Set up timeout signal
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cur.description]
                    return [dict(zip(columns, row)) for row in cur.fetchall()]
                return None
        except TimeoutError:
            print(f"⚠️  Query timed out after {timeout} seconds")
            return None
        except Exception as e:
            print(f"⚠️  Query failed: {e}")
            return None
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, old_handler)
    
    def get_all_tables(self) -> List[str]:
        """Get all user tables safely"""
        if self._table_cache is not None:
            return self._table_cache
            
        query = """
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public' 
        AND tablename NOT LIKE 'pg_%'
        AND tablename NOT LIKE 'sql_%'
        ORDER BY tablename
        """
        
        result = self.safe_execute(query, timeout=10)
        if result:
            tables = [row['tablename'] for row in result]
            self._table_cache = tables
            return tables
        return []
    
    def get_table_stats_safe(self, table_name: str) -> Dict[str, Any]:
        """Get statistics for a table safely"""
        try:
            # Quick row count with timeout
            count_query = f"SELECT COUNT(*) as count FROM {table_name}"
            result = self.safe_execute(count_query, timeout=5)
            
            if result and len(result) > 0:
                row_count = result[0]['count']
                
                # Get size info
                size_query = """
                SELECT 
                    pg_size_pretty(pg_total_relation_size(%s)) as size,
                    pg_total_relation_size(%s) as size_bytes
                """
                size_result = self.safe_execute(size_query, (table_name, table_name), timeout=5)
                
                if size_result and len(size_result) > 0:
                    return {
                        'table_name': table_name,
                        'row_count': row_count,
                        'size_pretty': size_result[0]['size'] or 'Unknown',
                        'size_bytes': size_result[0]['size_bytes'] or 0
                    }
                else:
                    return {
                        'table_name': table_name,
                        'row_count': row_count,
                        'size_pretty': 'Unknown',
                        'size_bytes': 0
                    }
            else:
                return {
                    'table_name': table_name,
                    'row_count': -1,
                    'size_pretty': 'Timeout',
                    'size_bytes': 0,
                    'error': 'Query timeout'
                }
        except Exception as e:
            return {
                'table_name': table_name,
                'row_count': -1,
                'size_pretty': 'Error',
                'size_bytes': 0,
                'error': str(e)
            }
    
    def get_active_processes(self) -> List[Dict[str, Any]]:
        """Get active processes safely"""
        query = """
        SELECT 
            pid,
            usename,
            application_name,
            client_addr,
            state,
            query_start,
            state_change,
            LEFT(query, 100) as query_preview,
            wait_event_type,
            wait_event
        FROM pg_stat_activity 
        WHERE state != 'idle' 
        AND pid != pg_backend_pid()
        ORDER BY query_start ASC
        """
        
        return self.safe_execute(query, timeout=10) or []
    
    def get_locks(self) -> List[Dict[str, Any]]:
        """Get locks safely"""
        query = """
        SELECT 
            l.pid,
            l.mode,
            l.granted,
            l.locktype,
            CASE 
                WHEN l.locktype = 'relation' THEN c.relname
                WHEN l.locktype = 'virtualxid' THEN l.virtualxid::text
                ELSE 'N/A'
            END as lock_object,
            a.usename,
            LEFT(a.query, 100) as query_preview
        FROM pg_locks l
        LEFT JOIN pg_class c ON l.relation = c.oid
        LEFT JOIN pg_stat_activity a ON l.pid = a.pid
        WHERE l.pid != pg_backend_pid()
        ORDER BY l.granted, l.pid
        """
        
        return self.safe_execute(query, timeout=10) or []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics safely"""
        queries = {
            'total_connections': "SELECT count(*) as count FROM pg_stat_activity",
            'active_connections': "SELECT count(*) as count FROM pg_stat_activity WHERE state != 'idle'",
            'idle_connections': "SELECT count(*) as count FROM pg_stat_activity WHERE state = 'idle'",
            'blocked_queries': "SELECT count(*) as count FROM pg_stat_activity WHERE wait_event_type IS NOT NULL",
            'total_locks': "SELECT count(*) as count FROM pg_locks",
            'blocked_locks': "SELECT count(*) as count FROM pg_locks WHERE NOT granted",
            'total_tables': "SELECT count(*) as count FROM pg_tables WHERE schemaname = 'public' AND tablename NOT LIKE 'pg_%'"
        }
        
        stats = {}
        for key, query in queries.items():
            result = self.safe_execute(query, timeout=5)
            if result and len(result) > 0:
                stats[key] = result[0]['count']
            else:
                stats[key] = 0
        
        return stats
    
    def kill_process(self, pid: int) -> bool:
        """Kill a specific process safely"""
        try:
            result = self.safe_execute("SELECT pg_terminate_backend(%s) as result", (pid,), timeout=5)
            if result and len(result) > 0:
                return result[0]['result']
            return False
        except Exception as e:
            print(f"❌ Failed to kill process {pid}: {e}")
            return False
    
    def cleanup_idle_transactions(self) -> List[int]:
        """Clean up idle transactions safely"""
        query = """
        SELECT pid, usename, state, query_start
        FROM pg_stat_activity 
        WHERE state = 'idle in transaction'
        AND pid != pg_backend_pid()
        """
        
        idle_processes = self.safe_execute(query, timeout=10) or []
        killed_pids = []
        
        for proc in idle_processes:
            pid = proc['pid']
            usename = proc['usename']
            query_start = proc['query_start']
            
            print(f"🔪 Killing idle transaction {pid} (user: {usename}, started: {query_start})")
            
            if self.kill_process(pid):
                killed_pids.append(pid)
                print(f"✅ Idle transaction {pid} killed successfully")
            else:
                print(f"❌ Failed to kill idle transaction {pid}")
        
        return killed_pids
    
    def kill_long_running_processes(self, threshold_minutes: int = 10) -> List[int]:
        """Kill long running processes safely"""
        query = """
        SELECT 
            pid,
            usename,
            state,
            query_start,
            EXTRACT(EPOCH FROM (now() - query_start))/60 as duration_minutes,
            LEFT(query, 100) as query_preview
        FROM pg_stat_activity 
        WHERE state != 'idle'
        AND query_start < now() - interval '%s minutes'
        AND pid != pg_backend_pid()
        ORDER BY query_start ASC
        """
        
        long_running = self.safe_execute(query, (threshold_minutes,), timeout=10) or []
        killed_pids = []
        
        for process in long_running:
            pid = process['pid']
            duration = process['duration_minutes']
            query_preview = process['query_preview']
            
            print(f"🔪 Killing process {pid} (running for {duration:.1f} minutes): {query_preview}")
            
            if self.kill_process(pid):
                killed_pids.append(pid)
                print(f"✅ Process {pid} killed successfully")
            else:
                print(f"❌ Failed to kill process {pid}")
        
        return killed_pids
    
    def print_report(self, verbose: bool = False, max_tables: int = 5):
        """Print comprehensive database health report safely"""
        print("\n" + "="*80)
        print("ROBUST DATABASE HEALTH REPORT")
        print("="*80)
        print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Database stats
        print("\n📊 DATABASE STATISTICS:")
        print("-" * 40)
        stats = self.get_database_stats()
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Table statistics (limited for safety)
        print(f"\n📋 TABLE STATISTICS (showing first {max_tables} tables):")
        print("-" * 40)
        tables = self.get_all_tables()
        if tables:
            for table in tables[:max_tables]:
                table_stats = self.get_table_stats_safe(table)
                if 'error' not in table_stats:
                    print(f"  {table}: {table_stats['row_count']} rows, {table_stats['size_pretty']}")
                else:
                    print(f"  {table}: Error - {table_stats['error']}")
            
            if len(tables) > max_tables:
                print(f"  ... and {len(tables) - max_tables} more tables")
        else:
            print("  No tables found or timeout occurred")
        
        # Active processes
        print("\n🔄 ACTIVE PROCESSES:")
        print("-" * 40)
        processes = self.get_active_processes()
        if processes:
            for proc in processes:
                duration = ""
                if proc['query_start']:
                    try:
                        now = datetime.now(proc['query_start'].tzinfo) if proc['query_start'].tzinfo else datetime.now()
                        duration_seconds = (now - proc['query_start']).total_seconds()
                        duration = f" (running for {duration_seconds:.1f}s)"
                    except:
                        duration = " (duration unavailable)"
                print(f"  PID {proc['pid']}: {proc['state']}{duration}")
                if verbose and proc['query_preview']:
                    print(f"    Query: {proc['query_preview']}")
        else:
            print("  No active processes found")
        
        # Locks
        print("\n🔒 LOCKS:")
        print("-" * 40)
        locks = self.get_locks()
        if locks:
            for lock in locks:
                status = "✅ GRANTED" if lock['granted'] else "❌ BLOCKED"
                print(f"  {status} - PID {lock['pid']}: {lock['mode']} on {lock['lock_object']}")
                if verbose and lock['query_preview']:
                    print(f"    Query: {lock['query_preview']}")
        else:
            print("  No locks found")
        
        print("\n" + "="*80)

def main_automated():
    print("\n=== AUTOMATED ROBUST DATABASE CLEANUP ===\n")
    checker = RobustDatabaseHealthChecker(DB_CONFIG, timeout_seconds=30)
    if not checker.connect():
        sys.exit(1)
    try:
        checker.print_report(verbose=True, max_tables=5)
        print("\n🧹 CLEANING UP IDLE TRANSACTIONS:")
        killed_idle = checker.cleanup_idle_transactions()
        print(f"✅ Killed {len(killed_idle)} idle transactions: {killed_idle}")
        print("\n🔪 KILLING PROCESSES RUNNING LONGER THAN 10 MINUTES:")
        killed_long = checker.kill_long_running_processes(10)
        print(f"✅ Killed {len(killed_long)} long running processes: {killed_long}")
        print("\n📊 FINAL STATUS:")
        checker.print_report(verbose=False, max_tables=3)
    finally:
        checker.disconnect()

if __name__ == "__main__":
    main_automated() 