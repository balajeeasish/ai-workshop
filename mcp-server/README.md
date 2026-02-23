# MCP Project Scaffolder

An MCP (Model Context Protocol) server that generates starter project structures for Python, Node.js, and Go. Built with [FastMCP](https://github.com/jlowin/fastmcp), containerized with Docker, designed to be consumed by [Claude Code](https://code.claude.com).

This is the companion repo for the freeCodeCamp article: **How to Build an MCP Server with Python, Docker, and Claude Code**.

Source code: https://github.com/balajeeasish/mcp-scaffolder

## Tools

- **scaffold_project** - Creates a new project directory with language-appropriate boilerplate files
- **list_templates** - Lists all available project templates and their contents

## Supported Languages

- Python (main.py, requirements.txt, tests/, .gitignore)
- Node.js (index.js, package.json, .gitignore)
- Go (main.go, go.mod, cmd/, internal/, .gitignore)

## Quick Start

### Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server.py
```

### Run with Docker

```bash
docker build -t mcp-scaffolder .
docker run -i --rm mcp-scaffolder
```

### Connect to Claude Code

```bash
claude mcp add scaffolder -- docker run -i --rm mcp-scaffolder
```

Then inside Claude Code, type `/mcp` to verify the connection and try:

```
Create a new Python project called "my-app"
```

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```

## Security Notes

- The Docker container does not mount your host filesystem by default. If you need the server to write files to your host, mount only the specific directory you need: `docker run -i --rm -v $(pwd)/projects:/app/projects mcp-scaffolder`
- Project names are validated against path traversal attacks (`..`, `/`, `\` are rejected)
- See the [AuthZed timeline of MCP security incidents](https://authzed.com/blog/timeline-mcp-breaches) for broader ecosystem security context

## License

MIT
