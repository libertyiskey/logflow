import json
import os

# Choose config file based on an environment variable
CONFIG_FILE_NAME = ".logflowconfig_test.json" if os.getenv("LOGFLOW_TEST") else ".logflowconfig.json"
CONFIG_FILE_PATH = os.path.join(os.path.expanduser("~"), CONFIG_FILE_NAME)

def load_config():
    if not os.path.exists(CONFIG_FILE_PATH):
        return {}
    with open(CONFIG_FILE_PATH, 'r') as file:
        return json.load(file)

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
    with open(CONFIG_FILE_PATH, 'w') as file:
        json.dump(config, file, indent=4)

def get_log_file_path():
    config = load_config()
    return config.get("log_file_path", "logs/logs.json")

def set_log_file_path(path):
    config = load_config()
    config["log_file_path"] = path
    save_config(config)


def ensure_log_directory_exists(log_file_path):
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        print(f"Log directory {log_dir} does not exist, creating it.")
        os.makedirs(log_dir, exist_ok=True)


def add_log_file_path_to_registry(log_file_path):
    """Add a new log file path to the registry in the configuration as an absolute path."""
    config = load_config()
    # Convert the log_file_path to an absolute path
    absolute_log_file_path = os.path.abspath(log_file_path)
    
    log_path_registry = set(config.get("log_path_registry", []))
    log_path_registry.add(absolute_log_file_path)
    
    config["log_path_registry"] = list(log_path_registry)
    save_config(config)

def get_log_path_registry():
    """Retrieve the list of all registered log file paths from the configuration."""
    config = load_config()
    return config.get("log_path_registry", [])

def remove_log_file_path_from_registry(log_file_path):
    """Remove a log file path from the registry in the configuration."""
    config = load_config()
    log_path_registry = set(config.get("log_path_registry", []))
    if log_file_path in log_path_registry:
        log_path_registry.remove(log_file_path)
        config["log_path_registry"] = list(log_path_registry)
        save_config(config)
