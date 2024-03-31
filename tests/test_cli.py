import pytest
import json
import tempfile
from logflow.cli import main as cli_main
from logflow.config_handler import set_log_file_path, add_log_file_path_to_registry, get_log_file_path
from datetime import datetime, timedelta
import sys
import os
import re

# Mock CLI arguments
def run_cli_test(args):
    sys.argv = ["cli.py"] + args.split()
    cli_main()

@pytest.fixture
def setup_cli_environment():
    temp_log_file = tempfile.NamedTemporaryFile(delete=False, mode='w')
    set_log_file_path(temp_log_file.name)

    # Simulate log entries for 10 different executions
    for i in range(10):  # Generate entries for 10 executions
        execution_id = f'exec-{10-i}'  # Ensure exec-10 is the most recent, exec-1 the oldest
        for j in range(5):  # 5 log entries per execution
            log_entry = {
                "level": "INFO",
                "message": f"Test log entry {j+1} from {execution_id}",
                "timestamp": (datetime.utcnow() - timedelta(days=i, hours=j)).isoformat(),  # Stagger timestamps within each execution
                "execution_id": execution_id,
                "success": j % 2 == 0  # Alternate success value to simulate a mix of successes and failures
            }
            json.dump(log_entry, temp_log_file)
            temp_log_file.write('\n')

    temp_log_file.close()
    add_log_file_path_to_registry(temp_log_file.name)
    yield temp_log_file.name
    os.remove(temp_log_file.name)

    
def test_cli_tail(capsys, setup_cli_environment):
    run_cli_test("tail -n 1")
    captured = capsys.readouterr()
    assert "Test log entry" in captured.out

def test_cli_search(capsys, setup_cli_environment):
    # Updated to use new searchable fields
    run_cli_test("search Test --level INFO --start_time 2021-01-01T00:00:00Z --end_time 2030-01-01T00:00:00Z")
    captured = capsys.readouterr()
    assert "Test log entry" in captured.out

def test_cli_list_log_paths(capsys, setup_cli_environment):
    run_cli_test("list")
    captured = capsys.readouterr()
    assert setup_cli_environment in captured.out
    

def test_cli_summarize(capsys, setup_cli_environment):
    run_cli_test("summarize -last 2")
    captured = capsys.readouterr()
    output = captured.out

    # Compile a regex pattern to match lines that exactly contain the execution IDs we're interested in
    exec_10_pattern = re.compile(r'^Execution ID: exec-10$', re.M)
    exec_9_pattern = re.compile(r'^Execution ID: exec-9$', re.M)
    exec_1_pattern = re.compile(r'^Execution ID: exec-1$', re.M)

    # Use the regex pattern to search within the output
    assert exec_10_pattern.search(output), "exec-10 should be present in the output"
    assert exec_9_pattern.search(output), "exec-9 should be present in the output"
    assert not exec_1_pattern.search(output), "exec-1 should not be present in the output"


    
def test_cli_select(capsys, setup_cli_environment):
    new_log_path = "/tmp/new_log_path.json"
    run_cli_test(f"select {new_log_path}")
    captured = capsys.readouterr()
    assert get_log_file_path() == new_log_path
    assert "Log file path set to" in captured.out

# Add more tests as needed for the new functionality
