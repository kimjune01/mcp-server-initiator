from mcp.server.fastmcp import FastMCP
import shutil
from pathlib import Path
import re
import subprocess

mcp = FastMCP("mcp-initiator")


@mcp.tool()
async def ping() -> str:
    """Ping the MCP Initiator server"""
    return "Pong MCP Initiator!!"


@mcp.tool()
async def initiate_mcp_server(server_name: str) -> str:
    """Initiate an MCP server"""
    # Check if server_name is safe (alphanumeric, dash, underscore only)
    if not re.match(r"^[\w\-]+$", server_name.strip()):
        raise ValueError(
            "Server name must only contain letters, numbers, dashes, or underscores, and no spaces."
        )
    # Define source and destination paths
    source_dir = Path(__file__).parent / "boiler"
    dest_dir = Path.home() / "Documents" / server_name
    if dest_dir.exists():
        raise FileExistsError(f"Directory {dest_dir} already exists.")
    try:
        shutil.copytree(source_dir, dest_dir)
        uv_sync_run = False
        # Recursively replace 'boiler' with server_name in all text files
        for file_path in dest_dir.rglob("*"):
            if file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    new_content = re.sub(
                        r"boiler", server_name, content, flags=re.IGNORECASE
                    )
                    if new_content != content:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        if not uv_sync_run:
                            subprocess.run(["uv", "sync"], cwd=dest_dir, check=True)
                            uv_sync_run = True
                except UnicodeDecodeError:
                    # Skip binary files
                    continue
        # Read and return the contents of claude-config.json
        config_path = dest_dir / "claude-config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"{config_path} does not exist.")
        with open(config_path, "r", encoding="utf-8") as f:
            config_contents = f.read()
        return config_contents
    except Exception as e:
        return f"Failed to initiate MCP server: {e}"


if __name__ == "__main__":
    mcp.run()
