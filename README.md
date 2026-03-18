# AI Workshop

A growing collection of hands-on AI projects — from container monitoring agents to MCP servers. Each project includes complete working code, Docker support, and production-ready configurations.

## Projects

| # | Project | Description | Stack |
|---|---------|-------------|-------|
| 1 | [MCP Server](./mcp-server/) | Production-ready Model Context Protocol server that scaffolds project structures. Built with FastMCP, containerized with Docker, integrated with Claude Code. | Python, FastMCP, Docker |
| 2 | [Docker Container Doctor](./docker-container-doctor/) | AI-powered agent that monitors Docker container logs, diagnoses errors using Claude, and auto-restarts containers when safe. | Python, Claude API, Docker |

## Getting Started

Each project is self-contained with its own README, dependencies, and Docker setup.

```bash
# Clone the repo
git clone https://github.com/balajeeasish/ai-workshop.git
cd ai-workshop

# Pick a project
cd docker-container-doctor   # or mcp-server
cp .env.example .env         # Add your API keys
pip install -r requirements.txt
```

## Repository Structure

```
ai-workshop/
├── mcp-server/                # MCP server with project scaffolding tools
├── docker-container-doctor/   # AI container monitoring agent
└── README.md
```

## Security

- API keys and secrets are stored in `.env` files (git-ignored)
- Each project includes a `.env.example` with placeholder values
- No credentials are committed to the repository

---

*Built by [Balajee Asish Brahmandam](https://github.com/balajeeasish)*
