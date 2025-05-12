from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("boiler")


@mcp.tool()
async def ping() -> str:
    """Ping the Boiler server"""
    return "Pong!"


if __name__ == "__main__":
    mcp.run()
