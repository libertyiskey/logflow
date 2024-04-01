
# [](https://ibb.co/yXyqqXL) Logflow Package

LogFlow is a logging library crafted for data engineers, facilitating tracking and organization of logs within data pipelines. Central to LogFlow's functionality is its decorator, @log_function_data, which allows for seamless, detailed logging across various components of data engineering projects.

## Key Features

**@Logflow Decorator** : At the core of LogFlow, this decorator automates detailed logging with rich contextual information, including project, flow, task identifiers, and custom metadata. It's tailored to capture every critical aspect of data processing activities, offering unparalleled clarity into your data engineering projects.

- **Project, Flow, and Task Context** : Tailor your logging to reflect the hierarchical structure of data pipelines. Log entries are enriched with identifiers for the project, flow, and task, providing clarity on the log's origin and making it easier to filter and analyze logs.
- **Versatile CLI Tool**: LogFlow elevates log management with its comprehensive CLI, designed to address the dynamic needs of data engineers:
Tail and Stream Logs: Effortlessly monitor your logs in real-time or stream them to keep tabs on ongoing processes with commands like logflow tail and logflow stream.
- **Error Handling and Success Tracking**: Automatically captures and logs exceptions, along with a success flag, facilitating quick identification of errors and their sources within your pipelines.

## Getting Started

### Installation

Install LogFlow using pip:

```bash
pip install LogFlow
```

### Quick Setup

1. **Logging Decorator**: Integrate logging into functions with `@log_function_data`, specifying the level, project ID, flow ID, task ID, and any custom metadata.

2. **CLI Commands**: The LogFlow CLI tool offers several commands for interacting with your logs:
    - `tail`: Display the last `n` log entries.
    - `stream`: Stream logs in real-time.
    - `search`: Search the logs for specific queries.
    - `list`: List all registered log paths.
    - `select`: Select a specific log file path for operations.

## Usage

### Decorator in Python Code

```python
from LogFlow.log_decorator import log_function_data

@log_function_data(level="INFO", project_id="Project123", flow_id="DataProcessing", task_id="TaskA", custom_metadata={"user": "admin"})
def process_data(data):
    # Function implementation
    pass
```

### CLI Tool
- **Tail Logs**: Dynamically monitor the latest log entries.

```
logflow tail -n 10
```

- **Stream Logs**: Keep tabs on your logs as they are generated, ideal for live monitoring of data processing tasks.

```
logflow stream
```

- **Advanced Log Search** : Utilize a simple yet powerful query language to search through logs. Filter by log level, date ranges, or custom queries within log content.

```
logflow search "error" --level ERROR --start_time "2021-01-01T00:00:00Z" --end_time "2021-01-31T23:59:59Z"
```

- **Manage Log Paths** : Effortlessly list all registered log file paths and select specific logs for operations, enabling you to switch contexts between different projects or log sources.

```
logflow list
logflow select /path/to/your/log.json
```

- **Advanced Log Searching**: 
The search command stands out with its ability to perform complex searches within your logs. Here’s how you can leverage it:
    - **Filter by Log Level**: Narrow down your search to logs of a specific severity.
    - **Date Range Filtering**: Specify start and end times to focus on logs generated within a certain period.
Custom Query String: Look for specific content within your logs, making it easier to pinpoint issues or events.
Example:

```
logflow search "database error" --level ERROR --start_time "2021-01-01T00:00:00" --end_time "2021-01-02T00:00:00"
```

This command fetches ERROR level logs containing the phrase "database error" that occurred between January 1st and 2nd, 2021.

## Configuration

Configuration for LogFlow can be done via a JSON file specifying the logging mode and details. The CLI tool `select` command allows for dynamic switching between log files or configurations.

## Contributing

Contributions to LogFlow are welcome! Feel free to open issues or pull requests to suggest improvements or add new features.

## License

LogFlow is licensed under the MIT License.
