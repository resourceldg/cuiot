#!/usr/bin/env python3
"""
Abstract Database Health Check and Cleanup Script
================================================

This script provides a generic database health monitoring and cleanup system
that works with any entity/table structure. It automatically detects:
- All tables in the database
- Active processes and their states
- Locks and deadlocks
- Long-running transactions
- Orphaned connections
- Database performance issues

Features:
- Entity-agnostic: Works with any table structure
- Automatic table detection
- Configurable cleanup strategies
- Extensible for new entity types
- Safe cleanup operations

Usage:
    python scripts/db_health_check.py [--cleanup] [--kill-long-running] [--verbose] [--auto]
"""

import argparse
import psycopg2
import sys
from datetime import datetime, timedelta
import os
from typing import List, Dict, Any, Optional

# Database connection settings
DB_CONFIG = {
    'host': 'postgres',  # Changed from 'localhost' to 'postgres' for Docker Compose
    'port': 5432,
    'database': 'viejos_trapos_db',
    'user': 'viejos_trapos_user',
    'password': 'viejos_trapos_pass'
}

class AbstractDatabaseHealthChecker:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.conn = None
        self._table_cache = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**self.config)
            self.conn.autocommit = True
            print("✅ Connected to database successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("🔌 Database connection closed")
    
    def get_all_tables(self) -> List[str]:
        """Get all user tables in the database (entity-agnostic)"""
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
        
        with self.conn.cursor() as cur:
            cur.execute(query)
            tables = [row[0] for row in cur.fetchall()]
            self._table_cache = tables
            return tables
    
    def get_table_stats(self, table_name: str) -> Dict[str, Any]:
        """Get statistics for any table (entity-agnostic)"""
        try:
            # Get row count
            count_query = f"SELECT COUNT(*) FROM {table_name}"
            with self.conn.cursor() as cur:
                cur.execute(count_query)
                row_count = cur.fetchone()[0]
            
            # Get table size
            size_query = """
            SELECT 
                pg_size_pretty(pg_total_relation_size(%s)) as size,
                pg_total_relation_size(%s) as size_bytes
            """
            with self.conn.cursor() as cur:
                cur.execute(size_query, (table_name, table_name))
                size_info = cur.fetchone()
            
            return {
                'table_name': table_name,
                'row_count': row_count,
                'size_pretty': size_info[0] if size_info else 'Unknown',
                'size_bytes': size_info[1] if size_info else 0
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
        """Get all active processes (entity-agnostic)"""
        query = """
        SELECT 
            pid,
            usename,
            application_name,
            client_addr,
            state,
            query_start,
            state_change,
            query,
            wait_event_type,
            wait_event
        FROM pg_stat_activity 
        WHERE state != 'idle' 
        AND pid != pg_backend_pid()
        ORDER BY query_start ASC
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    
    def get_locks(self) -> List[Dict[str, Any]]:
        """Get all locks (entity-agnostic)"""
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
            a.query
        FROM pg_locks l
        LEFT JOIN pg_class c ON l.relation = c.oid
        LEFT JOIN pg_stat_activity a ON l.pid = a.pid
        WHERE l.pid != pg_backend_pid()
        ORDER BY l.granted, l.pid
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    
    def get_long_running_transactions(self, threshold_minutes: int = 5) -> List[Dict[str, Any]]:
        """Get transactions running longer than threshold (entity-agnostic)"""
        query = """
        SELECT 
            pid,
            usename,
            application_name,
            state,
            query_start,
            EXTRACT(EPOCH FROM (now() - query_start))/60 as duration_minutes,
            query
        FROM pg_stat_activity 
        WHERE state != 'idle'
        AND query_start < now() - interval '%s minutes'
        AND pid != pg_backend_pid()
        ORDER BY query_start ASC
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query, (threshold_minutes,))
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics (entity-agnostic)"""
        queries = {
            'total_connections': "SELECT count(*) FROM pg_stat_activity",
            'active_connections': "SELECT count(*) FROM pg_stat_activity WHERE state != 'idle'",
            'idle_connections': "SELECT count(*) FROM pg_stat_activity WHERE state = 'idle'",
            'blocked_queries': "SELECT count(*) FROM pg_stat_activity WHERE wait_event_type IS NOT NULL",
            'total_locks': "SELECT count(*) FROM pg_locks",
            'blocked_locks': "SELECT count(*) FROM pg_locks WHERE NOT granted",
            'total_tables': f"SELECT count(*) FROM pg_tables WHERE schemaname = 'public' AND tablename NOT LIKE 'pg_%'"
        }
        
        stats = {}
        with self.conn.cursor() as cur:
            for key, query in queries.items():
                cur.execute(query)
                stats[key] = cur.fetchone()[0]
        
        return stats
    
    def get_table_locks(self, table_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get locks for specific table or all tables (entity-agnostic)"""
        if table_name:
            query = """
            SELECT 
                l.pid,
                l.mode,
                l.granted,
                a.usename,
                a.query
            FROM pg_locks l
            JOIN pg_class c ON l.relation = c.oid
            LEFT JOIN pg_stat_activity a ON l.pid = a.pid
            WHERE c.relname = %s
            AND l.pid != pg_backend_pid()
            """
            params = (table_name,)
        else:
            query = """
            SELECT 
                l.pid,
                l.mode,
                l.granted,
                c.relname as table_name,
                a.usename,
                a.query
            FROM pg_locks l
            JOIN pg_class c ON l.relation = c.oid
            LEFT JOIN pg_stat_activity a ON l.pid = a.pid
            WHERE l.locktype = 'relation'
            AND c.relname NOT LIKE 'pg_%'
            AND l.pid != pg_backend_pid()
            """
            params = ()
        
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    
    def kill_process(self, pid: int) -> bool:
        """Kill a specific process"""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT pg_terminate_backend(%s)", (pid,))
                result = cur.fetchone()[0]
                return result
        except Exception as e:
            print(f"❌ Failed to kill process {pid}: {e}")
            return False
    
    def kill_long_running_processes(self, threshold_minutes: int = 10) -> List[int]:
        """Kill processes running longer than threshold"""
        long_running = self.get_long_running_transactions(threshold_minutes)
        killed_pids = []
        
        for process in long_running:
            pid = process['pid']
            duration = process['duration_minutes']
            query = process['query'][:100] + "..." if len(process['query']) > 100 else process['query']
            
            print(f"🔪 Killing process {pid} (running for {duration:.1f} minutes): {query}")
            
            if self.kill_process(pid):
                killed_pids.append(pid)
                print(f"✅ Process {pid} killed successfully")
            else:
                print(f"❌ Failed to kill process {pid}")
        
        return killed_pids
    
    def cleanup_idle_transactions(self) -> List[int]:
        """Clean up idle transactions"""
        query = """
        SELECT pid, usename, state, query_start
        FROM pg_stat_activity 
        WHERE state = 'idle in transaction'
        AND pid != pg_backend_pid()
        """
        
        with self.conn.cursor() as cur:
            cur.execute(query)
            idle_processes = cur.fetchall()
        
        killed_pids = []
        for pid, usename, state, query_start in idle_processes:
            print(f"🔪 Killing idle transaction {pid} (user: {usename}, started: {query_start})")
            
            if self.kill_process(pid):
                killed_pids.append(pid)
                print(f"✅ Idle transaction {pid} killed successfully")
            else:
                print(f"❌ Failed to kill idle transaction {pid}")
        
        return killed_pids
    
    def cleanup_table_locks(self, table_name: str) -> List[int]:
        """Clean up locks for a specific table"""
        table_locks = self.get_table_locks(table_name)
        killed_pids = []
        
        for lock in table_locks:
            if not lock['granted']:  # Only kill processes with blocked locks
                pid = lock['pid']
                mode = lock['mode']
                print(f"🔪 Killing process {pid} with blocked {mode} lock on {table_name}")
                
                if self.kill_process(pid):
                    killed_pids.append(pid)
                    print(f"✅ Process {pid} killed successfully")
                else:
                    print(f"❌ Failed to kill process {pid}")
        
        return killed_pids
    
    def print_report(self, verbose: bool = False):
        """Print comprehensive database health report (entity-agnostic)"""
        print("\n" + "="*80)
        print("ABSTRACT DATABASE HEALTH REPORT")
        print("="*80)
        print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Database stats
        print("\n📊 DATABASE STATISTICS:")
        print("-" * 40)
        stats = self.get_database_stats()
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # Table statistics
        print("\n📋 TABLE STATISTICS:")
        print("-" * 40)
        tables = self.get_all_tables()
        for table in tables[:10]:  # Show first 10 tables
            table_stats = self.get_table_stats(table)
            if 'error' not in table_stats:
                print(f"  {table}: {table_stats['row_count']} rows, {table_stats['size_pretty']}")
            else:
                print(f"  {table}: Error - {table_stats['error']}")
        
        if len(tables) > 10:
            print(f"  ... and {len(tables) - 10} more tables")
        
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
                    except Exception as e:
                        duration = f" (duration unavailable: {e})"
                print(f"  PID {proc['pid']}: {proc['state']}{duration}")
                if verbose and proc['query']:
                    query_preview = proc['query'][:100] + "..." if len(proc['query']) > 100 else proc['query']
                    print(f"    Query: {query_preview}")
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
                if verbose and lock['query']:
                    query_preview = lock['query'][:100] + "..." if len(lock['query']) > 100 else lock['query']
                    print(f"    Query: {query_preview}")
        else:
            print("  No locks found")
        
        # Long running transactions
        print("\n⏰ LONG RUNNING TRANSACTIONS (>5 minutes):")
        print("-" * 40)
        long_running = self.get_long_running_transactions(5)
        if long_running:
            for proc in long_running:
                print(f"  PID {proc['pid']}: {proc['duration_minutes']:.1f} minutes")
                if verbose and proc['query']:
                    query_preview = proc['query'][:100] + "..." if len(proc['query']) > 100 else proc['query']
                    print(f"    Query: {query_preview}")
        else:
            print("  No long running transactions found")
        
        print("\n" + "="*80)

def main():
    parser = argparse.ArgumentParser(description='Abstract Database Health Check and Cleanup')
    parser.add_argument('--cleanup', action='store_true', help='Clean up idle transactions')
    parser.add_argument('--kill-long-running', type=int, metavar='MINUTES', 
                       help='Kill processes running longer than MINUTES')
    parser.add_argument('--cleanup-table', type=str, metavar='TABLE', 
                       help='Clean up locks for specific table')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--host', default='postgres', help='Database host')
    parser.add_argument('--port', type=int, default=5432, help='Database port')
    parser.add_argument('--database', default='viejos_trapos_db', help='Database name')
    parser.add_argument('--user', default='viejos_trapos_user', help='Database user')
    parser.add_argument('--password', default='viejos_trapos_pass', help='Database password')
    
    args = parser.parse_args()
    
    # Update config with command line arguments
    config = DB_CONFIG.copy()
    config.update({
        'host': args.host,
        'port': args.port,
        'database': args.database,
        'user': args.user,
        'password': args.password
    })
    
    checker = AbstractDatabaseHealthChecker(config)
    
    if not checker.connect():
        sys.exit(1)
    
    try:
        # Print health report
        checker.print_report(verbose=args.verbose)
        
        # Perform cleanup actions
        if args.cleanup:
            print("\n🧹 CLEANING UP IDLE TRANSACTIONS:")
            print("-" * 40)
            killed = checker.cleanup_idle_transactions()
            if killed:
                print(f"✅ Killed {len(killed)} idle transactions: {killed}")
            else:
                print("✅ No idle transactions to clean up")
        
        if args.cleanup_table:
            print(f"\n🧹 CLEANING UP LOCKS FOR TABLE '{args.cleanup_table}':")
            print("-" * 40)
            killed = checker.cleanup_table_locks(args.cleanup_table)
            if killed:
                print(f"✅ Killed {len(killed)} processes with locks on {args.cleanup_table}: {killed}")
            else:
                print(f"✅ No blocked locks found on table {args.cleanup_table}")
        
        if args.kill_long_running:
            print(f"\n🔪 KILLING PROCESSES RUNNING LONGER THAN {args.kill_long_running} MINUTES:")
            print("-" * 40)
            killed = checker.kill_long_running_processes(args.kill_long_running)
            if killed:
                print(f"✅ Killed {len(killed)} long running processes: {killed}")
            else:
                print("✅ No long running processes to kill")
        
        # Print final report if cleanup was performed
        if args.cleanup or args.kill_long_running or args.cleanup_table:
            print("\n📊 FINAL STATUS:")
            print("-" * 40)
            stats = checker.get_database_stats()
            print(f"  Active connections: {stats['active_connections']}")
            print(f"  Blocked queries: {stats['blocked_queries']}")
            print(f"  Blocked locks: {stats['blocked_locks']}")
    
    finally:
        checker.disconnect()

def main_automated():
    print("\n=== AUTOMATED ABSTRACT DATABASE CLEANUP ===\n")
    checker = AbstractDatabaseHealthChecker(DB_CONFIG)
    if not checker.connect():
        sys.exit(1)
    try:
        checker.print_report(verbose=True)
        print("\n🧹 CLEANING UP IDLE TRANSACTIONS:")
        killed_idle = checker.cleanup_idle_transactions()
        print(f"✅ Killed {len(killed_idle)} idle transactions: {killed_idle}")
        print("\n🔪 KILLING PROCESSES RUNNING LONGER THAN 10 MINUTES:")
        killed_long = checker.kill_long_running_processes(10)
        print(f"✅ Killed {len(killed_long)} long running processes: {killed_long}")
        print("\n📊 FINAL STATUS:")
        checker.print_report(verbose=True)
    finally:
        checker.disconnect()

if __name__ == "__main__":
    import sys
    if '--auto' in sys.argv or len(sys.argv) == 1:
        main_automated()
    else:
        main() 