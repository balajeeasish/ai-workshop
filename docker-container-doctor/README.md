# Docker Container Doctor 🩺

An AI-powered container monitoring agent that watches your Docker containers, detects errors in real-time, and uses Claude to diagnose issues and auto-fix when safe.

## How It Works

1. **Monitor** — Continuously polls container logs at a configurable interval
2. **Detect** — Scans logs for error patterns (exceptions, crashes, OOM, panics, etc.)
3. **Diagnose** — Sends error logs to Claude for root cause analysis and severity rating
4. **Fix** — Auto-restarts containers when Claude determines it's safe (high severity only)

## Project Structure

```
docker-container-doctor/
├── container_doctor.py   # Main monitoring agent
├── docker-compose.yml    # Full stack: doctor + sample containers
├── Dockerfile            # Docker image for the agent
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variable template
└── .env                  # Your API key (not committed)
```

## Quick Start

### 1. Clone and configure

```bash
cd docker-container-doctor
cp .env.example .env
# Add your Anthropic API key to .env
```

### 2. Run with Docker Compose

```bash
docker-compose up -d
```

This starts the doctor agent alongside sample containers (nginx, postgres) for monitoring.

### 3. Run standalone (monitor existing containers)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
export TARGET_CONTAINERS=my-app,my-db
python container_doctor.py
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | — | Your Anthropic API key (required) |
| `TARGET_CONTAINERS` | `web,api,db` | Comma-separated container names to monitor |
| `CHECK_INTERVAL` | `10` | Seconds between log checks |
| `LOG_LINES` | `50` | Number of recent log lines to analyze |
| `AUTO_FIX` | `true` | Enable/disable auto-restart on high severity issues |

## What Claude Analyzes

For each error detected, Claude returns:

- **Root cause** — specific explanation of the issue
- **Severity** — low / medium / high
- **Suggested fix** — actionable remediation steps
- **Auto-restart safe** — whether it's safe to restart the container
- **Config suggestions** — environment or config changes that might help

Only **high severity** issues with `auto_restart_safe: true` trigger an automatic restart.

## Requirements

- Python 3.12+
- Docker
- Anthropic API key with credits

## Tech Stack

- **Claude API** (`claude-sonnet-4-20250514`) — log analysis and diagnosis
- **Docker SDK for Python** — container management
- **Docker Compose** — orchestration
