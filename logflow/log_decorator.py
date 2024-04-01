import functools
import json
import os
import time
import traceback
from datetime import datetime, timezone
from uuid import uuid4
from .config_handler import get_log_file_path, add_log_file_path_to_registry
import contextlib
import threading

execution_context = threading.local()

@contextlib.contextmanager
def execution_logger():
    if not hasattr(execution_context, 'execution_id'):
        execution_context.execution_id = str(uuid4())
    try:
        yield execution_context.execution_id
    finally:
        pass 

def ensure_directory_exists(path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)

def log_to_json(log_entry):
    log_file_path = get_log_file_path()
    ensure_directory_exists(log_file_path)
    with open(log_file_path, 'a', encoding='utf-8') as file:
        json.dump(log_entry, file)
        file.write('\n')
    add_log_file_path_to_registry(log_file_path)

def logflow(level='INFO', project_id=None, flow_id=None, task_id=None, custom_metadata=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with execution_logger() as execution_id:
                log_entry = {
                    'execution_id': execution_id,
                    'level': level,
                    'project_id': project_id,
                    'function_name': func.__name__,
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'args': args,
                    'kwargs': kwargs,
                    'flow_id': flow_id,
                    'task_id': task_id,
                    'custom_metadata': custom_metadata if custom_metadata else {},
                }
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    log_entry['execution_time'] = f"{end_time - start_time:.2f} seconds"
                    log_entry['result'] = result
                    log_entry['success'] = True
                except Exception as e:
                    end_time = time.time()
                    log_entry['execution_time'] = f"{end_time - start_time:.2f} seconds"
                    log_entry['error'] = str(e)
                    log_entry['traceback'] = traceback.format_exc()
                    log_entry['success'] = False
                    raise
                finally:
                    log_to_json(log_entry)
                return result
        return wrapper
    return decorator
