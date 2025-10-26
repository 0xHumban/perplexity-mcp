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

## Available Features

The Perplexity MCP server provides four main tools to interact with the Perplexity AI API:

### 1. `ask_perplexity` - Standard Search

Main tool for performing web searches via Perplexity AI.

**How it works:**
- Sends a query to Perplexity AI to get up-to-date information from the web
- Returns a formatted response with cited sources
- Uses the default model (sonar) unless otherwise specified


**Use cases:**
- Search for recent or real-time information
- Get answers based on multiple web sources
- Verify facts or current statistics

**Example:**
```
#ask_perplexity
What are the latest AI developments in October 2024?
```

---

### 2. `ask_perplexity_exact_response` - Unmodified Response

Returns the exact response from Perplexity AI without any modification or reformatting.

**How it works:**
- Similar to `ask_perplexity` but preserves Perplexity's original response
- No additional processing is applied
- Ideal when you want Perplexity's raw answer


**Use cases:**
- When you want to see exactly what Perplexity responded
- To avoid any interpretation or reformatting by the assistant
- Get citations and sources exactly as Perplexity provides them

**Example:**
```
#ask_perplexity_exact_response
Search for the latest tech news in France
```

---

### 3. `ask_perplexity_for_instructions` - Instructions Mode

Designed to obtain detailed and executable instructions on a complex topic.

**How it works:**
- Uses a special pedagogical preprompt that guides Perplexity to provide structured instructions
- Ideal for learning or understanding technical concepts
- Returns detailed steps, code examples, and clear explanations


**Use cases:**
- Learn a new concept or technology
- Get a step-by-step guide to accomplish a task
- Understand complex topics with practical examples
- Generate example code with detailed explanations

**Example:**
```
#ask_perplexity_for_instructions
Create a REST API server in Go for my books database
```

---

### 4. `ask_perplexity_to_learn` - Learning Mode

Pedagogical tool specially designed for learning complex topics.

**How it works:**
- Uses an advanced pedagogical preprompt that structures the response to facilitate learning
- Breaks down concepts into logical steps
- Provides analogies, concrete examples, and comprehension checks
- Uses the reasoning model by default for more in-depth explanations


**Response structure:**
1. Simple overview of the concept
2. Breakdown into logical steps (3-7 steps)
3. For each step: simple explanation + concrete example + commented code
4. Checkpoints to verify understanding
5. Summary of key points and tips to go further

**Use cases:**
- Learning complex computer science concepts (algorithms, data structures, etc.)
- Understanding mathematical principles
- Studying new technologies or frameworks
- Self-directed learning on technical topics

**Example:**
```
#ask_perplexity_to_learn
Teach me arithmetic coding step by step with code examples in Go
```

---

### Available Sonar Models

All tools support the following models:

- **`sonar`** (default for ask_perplexity and ask_perplexity_exact_response)
  - Fast, general-purpose search
  - Good balance between speed and quality
  - Ideal for most queries

- **`sonar-pro`**
  - Enhanced accuracy and depth
  - More sources and analysis
  - Recommended for important searches

- **`sonar-deep-research`**
  - Comprehensive and thorough research
  - Complete analysis of multiple sources
  - For serious research projects

- **`sonar-reasoning`** (default for ask_perplexity_for_instructions and ask_perplexity_to_learn)
  - Advanced reasoning capabilities
  - Better for complex explanations
  - Ideal for learning and instructions

- **`sonar-reasoning-pro`**
  - Premium reasoning with extended context
  - Most powerful for complex tasks
  - Best understanding and explanation


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
