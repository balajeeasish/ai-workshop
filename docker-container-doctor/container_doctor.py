import docker
import json
import time
import logging
import os
from datetime import datetime
from anthropic import Anthropic

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

client = Anthropic()
docker_client = None

def get_docker_client():
    """Lazily initialize Docker client."""
    global docker_client
    if docker_client is None:
        docker_client = docker.from_env()
    return docker_client

TARGET_CONTAINERS = os.getenv("TARGET_CONTAINERS", "").split(",")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "10"))
LOG_LINES = int(os.getenv("LOG_LINES", "50"))
AUTO_FIX = os.getenv("AUTO_FIX", "true").lower() == "true"

def get_container_logs(container_name):
    """Fetch last N lines from a container."""
    try:
        container = get_docker_client().containers.get(container_name)
        logs = container.logs(tail=LOG_LINES, timestamps=False).decode("utf-8")
        return logs
    except Exception as e:
        logger.error(f"Failed to fetch logs for {container_name}: {e}")
        return None

def detect_errors(logs):
    """Check if logs contain error patterns."""
    error_patterns = [
        "error", "exception", "traceback", "failed", "crash",
        "fatal", "panic", "segmentation fault", "out of memory"
    ]
    logs_lower = logs.lower()
    for pattern in error_patterns:
        if pattern in logs_lower:
            return True
    return False

def diagnose_with_claude(container_name, logs):
    """Send logs to Claude for diagnosis."""
    prompt = f"""You are a DevOps expert analyzing container logs.

Container: {container_name}
Timestamp: {datetime.now().isoformat()}

Recent logs:
---
{logs}
---

Analyze these logs and provide:
1. Root cause (be specific)
2. Severity (low/medium/high)
3. Suggested fix (be actionable)
4. Is it safe to auto-restart? (yes/no)
5. Any environment variables or config that might help?

Keep your response JSON-like for parsing:
{{
    "root_cause": "...",
    "severity": "...",
    "suggested_fix": "...",
    "auto_restart_safe": true/false,
    "config_suggestions": ["...", "..."]
}}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text

def parse_diagnosis(diagnosis_text):
    """Extract JSON from Claude's response."""
    try:
        start = diagnosis_text.find("{")
        end = diagnosis_text.rfind("}") + 1
        if start >= 0 and end > start:
            json_str = diagnosis_text[start:end]
            return json.loads(json_str)
    except Exception as e:
        logger.error(f"Failed to parse diagnosis: {e}")
    return None

def apply_fix(container_name, diagnosis):
    """Apply auto-fixes if safe."""
    if not AUTO_FIX or not diagnosis.get("auto_restart_safe"):
        logger.info(f"Skipping auto-fix for {container_name} (unsafe or disabled)")
        return False

    try:
        container = get_docker_client().containers.get(container_name)
        logger.info(f"Restarting container {container_name}...")
        container.restart()
        logger.info(f"Container {container_name} restarted successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to restart {container_name}: {e}")
        return False

def monitor_containers():
    """Main monitoring loop."""
    logger.info(f"Starting Container Doctor for: {TARGET_CONTAINERS}")

    while True:
        for container_name in TARGET_CONTAINERS:
            container_name = container_name.strip()
            if not container_name:
                continue

            logs = get_container_logs(container_name)
            if not logs:
                continue

            if detect_errors(logs):
                logger.warning(f"Errors detected in {container_name}")
                diagnosis_text = diagnose_with_claude(container_name, logs)
                logger.info(f"Diagnosis: {diagnosis_text}")

                diagnosis = parse_diagnosis(diagnosis_text)
                if diagnosis:
                    if diagnosis.get("severity") == "high":
                        apply_fix(container_name, diagnosis)
                    else:
                        logger.info(f"Low/medium severity issue in {container_name}, skipping auto-fix")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        monitor_containers()
    except KeyboardInterrupt:
        logger.info("Container Doctor shutting down")
