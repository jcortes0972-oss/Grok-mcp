import os
from fastmcp import FastMCP

# Initialize the MCP app
app = FastMCP("BrowserConnector")

@app.tool()
def hello_world() -> str:
    """Returns a simple greeting message to verify connection."""
    return "Hello from your web-hosted Render server! The link works perfectly."

if __name__ == "__main__":
    # Render provides a PORT automatically, which we read here
    port = int(os.environ.get("PORT", 8080))
    app.run(transport="sse", host="0.0.0.0", port=port)
