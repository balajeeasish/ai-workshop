# AI Workshop

A collection of hands-on tutorials and examples for AI development, agent building, and modern tooling. Each tutorial includes complete working code, security considerations, and production-ready configurations.

## 🚀 Tutorials

### ✅ [MCP Server with Python](./mcp-server/) - **COMPLETE**
A production-ready Model Context Protocol (MCP) server that scaffolds project structures. Built with FastMCP, containerized with Docker, and integrated with Claude Code.

**Features:**
- Project scaffolding for Python, Node.js, and Go
- Path traversal protection and input validation
- Docker containerization for reproducible deployment
- Claude Code integration with full terminal workflow
- Comprehensive security considerations

**Quick Start:**
```bash
cd mcp-server
pip install -r requirements.txt
python server.py
```

*Coming soon:*
- React Dashboard with AI Integration
- FastAPI with OpenAI Integration  
- Docker Multi-Stage Builds
- Agent Security Best Practices

## 🛠️ Tech Stack

- **Python**: FastMCP, Docker, Claude Code
- **JavaScript**: React, Node.js, modern tooling
- **DevOps**: Docker, GitHub Actions, security scanning
- **AI**: OpenAI, Anthropic, custom agents

## 🔒 Security Focus

Every tutorial includes:
- Input validation and sanitization
- Path traversal protection
- Least-privilege token usage
- Real-world CVE examples
- Production deployment considerations

## 📁 Structure

```
ai-workshop/
├── mcp-server/          # ✅ COMPLETE: MCP server tutorial
│   ├── server.py        # Main MCP server with scaffolding tools
│   ├── Dockerfile       # Container configuration
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Detailed setup and usage guide
├── react-dashboard/       # Planned: React + AI tutorial  
├── fastapi-integration/  # Planned: API + AI tutorial
├── .gitignore            # Excludes "How to" articles and common files
└── README.md            # This file
```

## 🎯 Learning Goals

- Build production-ready AI tools
- Understand security implications
- Master modern development workflows
- Create portfolio-worthy projects

---

*Built by [Balajee Asish Brahmandam](https://github.com/balajeeasish)*
