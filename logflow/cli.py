import argparse
import json
import os
import time
from datetime import datetime
from datetime import timezone
from dateutil import parser as dateutil_parser
from logflow.config_handler import get_log_path_registry, set_log_file_path, get_log_file_path

def tail_logs(args):
    """Display the last `n` log entries."""
    log_file_path = get_log_file_path()
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[-args.n:]
            for line in lines:
                print(json.dumps(json.loads(line), indent=2))
    except FileNotFoundError:
        print(f"No logs found at {log_file_path}.")

def stream_logs(args):
    """Stream logs in real-time."""
    log_file_path = get_log_file_path()
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            file.seek(0, os.SEEK_END)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                print(json.dumps(json.loads(line), indent=2))
    except FileNotFoundError:
        print(f"No logs found at {log_file_path}.")

def search_logs(args):
    log_file_path = get_log_file_path()
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            logs = [json.loads(line) for line in file]

        if args.start_time:
            start_time = dateutil_parser.parse(args.start_time).replace(tzinfo=timezone.utc)

        if args.end_time:
            end_time = dateutil_parser.parse(args.end_time).replace(tzinfo=timezone.utc)

        filtered_logs = []
        for log in logs:
            # Ensure log timestamp is offset-aware and set to UTC
            log_time = dateutil_parser.parse(log['timestamp'])
            if log_time.tzinfo is None or log_time.tzinfo.utcoffset(log_time) is None:
                log_time = log_time.replace(tzinfo=timezone.utc)
            
            if args.start_time and log_time < start_time:
                continue
            if args.end_time and log_time > end_time:
                continue
            if args.level and log['level'] != args.level.upper():
                continue
            filtered_logs.append(log)

        for log_entry in filtered_logs:
            if args.query.lower() in json.dumps(log_entry).lower():
                print(json.dumps(log_entry, indent=2))

    except FileNotFoundError:
        print(f"No logs found at {log_file_path}.")

def list_log_paths(args):
    """List all registered log file paths."""
    paths = get_log_path_registry()
    if not paths:
        print("No registered log paths found.")
        return
    for path in paths:
        print(path)

def select_log_path(args):
    """Select a specific log file path for the CLI to use."""
    set_log_file_path(args.path)
    print(f"Log file path set to: {args.path}")
    
def summarize_executions(args):
    last_n = args.last  # Number of last executions to display
    log_file_path = get_log_file_path()
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            logs = [json.loads(line) for line in file]

        # Organize logs by execution_id
        executions = {}
        for log in logs:
            exec_id = log.get('execution_id')
            if exec_id not in executions:
                executions[exec_id] = {'success': 0, 'failure': 0, 'errors': [], 'latest_timestamp': None}

            log_timestamp = dateutil_parser.parse(log['timestamp'])
            current_latest = executions[exec_id]['latest_timestamp']
            if current_latest is None or log_timestamp > current_latest:
                executions[exec_id]['latest_timestamp'] = log_timestamp

            if log['success']:
                executions[exec_id]['success'] += 1
            else:
                executions[exec_id]['failure'] += 1
                if 'error' in log:
                    executions[exec_id]['errors'].append(log['error'])

        # Sort executions by the latest_timestamp and select the last N
        sorted_exec_ids = sorted(executions.keys(), key=lambda eid: executions[eid]['latest_timestamp'], reverse=True)[:last_n]

        # Print summary for the last N executions
        for exec_id in sorted_exec_ids:
            summary = executions[exec_id]
            print(f"Execution ID: {exec_id}")
            print(f"Success: {summary['success']}, Failure: {summary['failure']}")
            if summary['errors']:
                print("Errors:")
                for error in summary['errors']:
                    print(f"  - {error}")
            print()

    except FileNotFoundError:
        print(f"No logs found at {log_file_path}.")


def main():
    parser = argparse.ArgumentParser(description="LogFlow CLI Tool - A powerful logging CLI for managing and analyzing logs.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', help='Available commands:\n')

    tail_parser = subparsers.add_parser('tail', help='Display the last n log entries.\nUsage: tail -n [number]\n')
    tail_parser.add_argument('-n', type=int, default=10, help='Number of log entries to display.')
    tail_parser.set_defaults(func=tail_logs)

    stream_parser = subparsers.add_parser('stream', help='Stream logs in real-time.\nUsage: stream\n')
    stream_parser.set_defaults(func=stream_logs)

    list_parser = subparsers.add_parser('list', help='List all registered log file paths')
    list_parser.set_defaults(func=list_log_paths)

    select_parser = subparsers.add_parser('select', help='Select a specific log file path')
    select_parser.add_argument('path', type=str, help='The log file path to use')
    select_parser.set_defaults(func=select_log_path)
    
    search_parser = subparsers.add_parser('search', help='Search logs for a query with additional filters.\nUsage: search [query] --level [LEVEL] --start_time [START] --end_time [END]\n')
    search_parser.add_argument('query', type=str, help='Query string to search for in logs.')
    search_parser.add_argument('--level', type=str, help='Filter logs by level (e.g., INFO, ERROR).')
    search_parser.add_argument('--start_time', type=str, help='Filter logs after a specific start time (ISO format).')
    search_parser.add_argument('--end_time', type=str, help='Filter logs before a specific end time (ISO format).')
    search_parser.set_defaults(func=search_logs)
    
    summarize_parser = subparsers.add_parser('summarize', help='Summarize recent pipeline executions')
    summarize_parser.add_argument('-last', type=int, default=3, help='Number of last executions to summarize (default: 3)')
    summarize_parser.set_defaults(func=summarize_executions)
    
    # Parse arguments
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
