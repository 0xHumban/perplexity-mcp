# perplexity-mcp

A Perplexity AI MCP (Model Context Protocol) server implementation that enables AI assistants to search the web and get real-time information through Perplexity's Sonar models.


## Motivation

This project was created to utilize the $5 credits from Perplexity's Pro plan (free for students: [perplexity link](https://plex.it/referrals/O1P7124D)), providing an easy way to access web search capabilities through MCP-compatible AI assistants.


## Features

- 🌐 Web search capabilities through Perplexity AI
- 🔍 Multiple Sonar models support (sonar, sonar-pro, sonar-deep-research, sonar-reasoning, sonar-reasoning-pro)
- 🚀 Easy integration with VS Code and other MCP clients
- 📚 Citation support for sources

## Prerequisites

- Python 3.12 or higher
- UV package manager
- Perplexity API key ([Get one here](https://www.perplexity.ai/settings/api))

## Installation

### Method 1: No Installation Required (Recommended)

You can run perplexity-mcp directly without any installation using `uv tool run`. Just install UV and configure VS Code (see Configuration section below) - uv will handle everything automatically!

```sh
# Install UV package manager first
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or
brew install uv  # macOS with Homebrew
```

### Method 2: Development Install

For development or to contribute:

#### 1. Install UV Package Manager

```sh
# macOS (Homebrew)
brew install uv

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux (Direct)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Clone the repository

```sh
git clone https://github.com/0xHumban/perplexity-mcp.git
cd perplexity-mcp
```

#### 3. Install dependencies

```sh
uv sync
```

## Configuration

### For VS Code

>NOTE: **To add it globaly**: Create / Update the gloabl config file: `~/.config/Code/User/mcp.json`

#### If you used Method 1 (No Installation - Recommended):

Create or edit `.vscode/mcp.json` in your workspace:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "perplexity-key",
      "description": "API Key for Perplexity AI",
      "password": true
    }
  ],
  "servers": {
    "perplexity-mcp": {
      "command": "uv",
      "args": [
        "tool", "run", "--from",
        "git+https://github.com/0xHumban/perplexity-mcp.git",
        "perplexity-mcp"
      ],
      "env": {
        "PERPLEXITY_API_KEY": "${input:perplexity-key}"
      }
    }
  }
}
```

This method runs the tool directly from GitHub without any prior installation!

#### If you used Method 2 (Development Install):

Create or edit `.vscode/mcp.json` in your workspace:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "perplexity-key",
      "description": "API Key for Perplexity AI",
      "password": true
    }
  ],
  "servers": {
    "perplexity-mcp": {
      "command": "uv",
      "args": [
        "run",
        "perplexity-mcp"
      ],
      "cwd": "/path/to/perplexity-mcp",
      "env": {
        "PERPLEXITY_API_KEY": "${input:perplexity-key}"
      }
    }
  }
}
```

Replace `/path/to/perplexity-mcp` with the actual path to your cloned repository.

---

Then:
1. Reload VS Code window
2. Enter your Perplexity API key when prompted

### For other MCP clients

Set the environment variable:

```sh
export PERPLEXITY_API_KEY="your-api-key-here"
```

Then run:

```sh
uv run perplexity-mcp
```

## Usage

Once configured, you can use the `ask_perplexity` tool in your AI assistant:

```python
# Example prompt
"Use Perplexity to search for the latest news about AI developments"
```

Available models:
- `sonar` (default) - Fast, general-purpose search
- `sonar-pro` - Enhanced accuracy and depth
- `sonar-deep-research` - Comprehensive research
- `sonar-reasoning` - Advanced reasoning capabilities
- `sonar-reasoning-pro` - Premium reasoning with extended context

## Development

### Project Structure

```
perplexity-mcp/
├── perplexity_mcp/
│   ├── __init__.py
│   ├── server.py       # Main MCP server implementation
│   └── cli.py
├── pyproject.toml      # Project configuration
├── uv.lock            # Dependency lock file
└── README.md
```


## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
