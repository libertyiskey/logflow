import pytest
import json
import tempfile
import os
from logflow.log_decorator import logflow
from logflow.config_handler import CONFIG_FILE_PATH, set_log_file_path

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Set environment variable to use the test config
    os.environ["LOGFLOW_TEST"] = "1"
    # Clear test configuration before each test
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)
    # Setup for a test
    yield
    # Teardown after a test
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)
    del os.environ["LOGFLOW_TEST"]

# Assuming these are your decorated functions in your package
@logflow(level="INFO", project_id="TestProject", flow_id="TestFlow", task_id="TestTask")
def success_task():
    return "Task succeeded."

@logflow(level="ERROR", project_id="ErrorProject", flow_id="ErrorFlow", task_id="ErrorTask", custom_metadata={"reason": "Test error"})
def failing_task():
    raise ValueError("Simulated Task Failure")

# Fixture to handle dynamic project configurations
@pytest.fixture(params=["project1", "project2"])
def project_environment(tmp_path, request):
    # Setup different environments based on the parameter
    project_id = request.param
    config_file = tmp_path / f"{project_id}_config.json"
    print(config_file)
    log_file = tmp_path / f"{project_id}_logs.json"

    # Example configuration for each project
    if project_id == "project1":
        config = {"mode": "local", "log_file": str(log_file)}
    else:  # Assume project2 or other scenarios
        config = {"mode": "local", "log_file": str(log_file)}

    # Save the project-specific configuration
    with open(config_file, 'w') as f:
        json.dump(config, f)

    # Set the log file path for the current project environment
    set_log_file_path(str(log_file))
    
    yield str(log_file)  # Yield the path to the log file for reading logs in tests

def read_log_entries(log_file_path):
    with open(log_file_path, 'r') as file:
        return [json.loads(line) for line in file]

# Example test using the project_environment fixture
def test_success_task_creates_log(project_environment):
    log_file_path = project_environment
    success_task()
    logs = read_log_entries(log_file_path)
    assert len(logs) == 1
    assert logs[0]['success'] is True
    assert logs[0]['project_id'] == "TestProject"

def test_failing_task_creates_log(project_environment):
    log_file_path = project_environment
    with pytest.raises(ValueError):
        failing_task()
    logs = read_log_entries(log_file_path)
    assert len(logs) == 1
    assert logs[0]['success'] is False
    assert logs[0]['custom_metadata'] == {"reason": "Test error"}
