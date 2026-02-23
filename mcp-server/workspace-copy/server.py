# server.py
from mcp.server.fastmcp import FastMCP
import os
import json

mcp = FastMCP("project-scaffolder")

# Templates for different languages
TEMPLATES = {
    "python": {
        "files": {
            "main.py": '"""Entry point."""\n\n\ndef main():\n    print("Hello, world!")\n\n\nif __name__ == "__main__":\n    main()\n',
            "requirements.txt": "",
            "README.md": "# {name}\n\nA Python project.\n\n## Setup\n\n```bash\npip install -r requirements.txt\npython main.py\n```\n",
            ".gitignore": "__pycache__/\n*.pyc\n.venv/\n",
        },
        "dirs": ["tests"],
    },
    "node": {
        "files": {
            "index.js": 'console.log("Hello, world!");\n',
            "package.json": '{{\n  "name": "{name}",\n  "version": "1.0.0",\n  "main": "index.js"\n}}\n',
            "README.md": "# {name}\n\nA Node.js project.\n\n## Setup\n\n```bash\nnpm install\nnode index.js\n```\n",
            ".gitignore": "node_modules/\n",
        },
        "dirs": [],
    },
    "go": {
        "files": {
            "main.go": 'package main\n\nimport "fmt"\n\nfunc main() {{\n\tfmt.Println("Hello, world!")\n}}\n',
            "go.mod": "module {name}\n\ngo 1.21\n",
            "README.md": "# {name}\n\nA Go project.\n\n## Setup\n\n```bash\ngo run main.go\n```\n",
            ".gitignore": "bin/\n",
        },
        "dirs": ["cmd", "internal"],
    },
}


@mcp.tool()
def scaffold_project(name: str, language: str) -> str:
    """Create a new project directory structure.

    Args:
        name: The project name (used as the directory name)
        language: The programming language - one of: python, node, go
    """
    language = language.lower().strip()

    # Path traversal protection
    if ".." in name or "/" in name or "\\" in name:
        return json.dumps({"error": "Invalid project name"})

    if language not in TEMPLATES:
        return json.dumps({
            "error": f"Unsupported language: {language}",
            "supported": list(TEMPLATES.keys()),
        })

    template = TEMPLATES[language]
    base_path = os.path.join(os.getcwd(), name)

    if os.path.exists(base_path):
        return json.dumps({
            "error": f"Directory already exists: {name}",
        })

    # Create the project directory
    os.makedirs(base_path, exist_ok=True)

    # Create subdirectories
    for dir_name in template["dirs"]:
        os.makedirs(os.path.join(base_path, dir_name), exist_ok=True)

    # Create files
    created_files = []
    for filename, content in template["files"].items():
        filepath = os.path.join(base_path, filename)
        formatted_content = content.replace("{name}", name)
        with open(filepath, "w") as f:
            f.write(formatted_content)
        created_files.append(filename)

    return json.dumps({
        "status": "created",
        "path": base_path,
        "language": language,
        "files": created_files,
        "directories": template["dirs"],
    })


@mcp.tool()
def list_templates() -> str:
    """List all available project templates and their contents."""
    result = {}
    for lang, template in TEMPLATES.items():
        result[lang] = {
            "files": list(template["files"].keys()),
            "directories": template["dirs"],
        }
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
