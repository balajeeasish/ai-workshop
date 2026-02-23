FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# MCP servers over stdio need unbuffered output
ENV PYTHONUNBUFFERED=1

# The server reads from stdin and writes to stdout
CMD ["python", "server.py"]
