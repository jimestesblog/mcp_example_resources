# MCP Example Resources

Example resource implementations for MCP Server applications, providing both public HTTP resources and private MCP server resources with parameterization support.

## Features

- **Public HTTP Resources**: Access public HTTP/HTTPS resources with automatic content fetching
- **Private MCP Resources**: Server-side resources with custom logic and parameterization
- **Parameter Support**: Resources can accept parameters for dynamic content generation
- **Multiple Resource Types**: Support for CSV, TXT, JSON, and other content types

## Installation

### For End Users

Install the package directly from PyPI (when published):

```bash
pip install mcp-example-resources
```

### For Development or Local Installation

#### Option 1: Install from Source (Recommended)

1. Clone or download the project:
   ```bash
   git clone https://github.com/example/mcp-example-resources.git
   cd mcp-example-resources
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

#### Option 2: Build and Install Package

1. Navigate to the project directory:
   ```bash
   cd path/to/mcp_example_resources
   ```

2. Build the package:
   ```bash
   python -m build
   ```
   *Note: You may need to install build tools first: `pip install build`*

3. Install the built package:
   ```bash
   pip install dist/mcp_example_resources-0.1.0-py3-none-any.whl
   ```

#### Option 3: Direct Installation from Local Directory

If you have the source code locally:

```bash
cd path/to/mcp_example_resources
pip install .
```

### Verification

To verify the installation was successful:

```bash
python -c "from mcp_example_resources import HttpResource, ExamplePrivateResources; print('Installation successful!')"
```

## Usage

The package provides two main resource classes:

### HttpResource

For accessing public HTTP/HTTPS resources:

```python
from mcp_example_resources import HttpResource

# Initialize with resource configuration
config = {
    "name": "http_resources",
    "params": {
        "resources": [
            {
                "name": "weather_data",
                "description": "Static weather data",
                "type": "csv",
                "access": "public",
                "uri": "https://raw.githubusercontent.com/example/data.csv",
                "resource_parameters": []
            }
        ]
    }
}

http_resource = HttpResource(config)
```

### ExamplePrivateResources

For private MCP server resources with custom logic:

```python
from mcp_example_resources import ExamplePrivateResources

# Initialize with parameterized resource configuration
config = {
    "name": "example_private_resources",
    "params": {
        "resources": [
            {
                "name": "sample_parameterized_resource",
                "description": "Sample parameterized resource",
                "function": "_sample_parameterized_resource",
                "type": "txt",
                "access": "mcp_server",
                "uri": "//sampledata/{client}/",
                "resource_parameters": [
                    {
                        "name": "client",
                        "description": "Client ID",
                        "allowed_values": "string"
                    }
                ]
            }
        ]
    }
}

private_resource = ExamplePrivateResources(config)
```

## Requirements

- Python 3.8+
- pydantic>=2.0.0
- httpx>=0.24.0

## Resource Types

Supported resource types include:
- `csv` - Comma-separated values
- `txt` - Plain text
- `json` - JSON data
- `xml` - XML documents
- `html` - HTML content
- `pdf` - PDF documents

## License

MIT License