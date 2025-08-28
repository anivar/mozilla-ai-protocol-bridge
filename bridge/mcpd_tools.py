"""Simplified mcpd tools module demonstrating the agent-factory approach.

This module shows the core concepts from agent-factory PR #310
for integrating with mcpd's REST API instead of using MCPStdio.
"""

import httpx
from typing import Any, Dict, Optional, List


async def mcpd_call_tool(
    server: str, 
    tool: str, 
    args: Dict[str, Any], 
    mcpd_url: str = "http://localhost:8090",
    headers: Optional[Dict[str, str]] = None
) -> str:
    """Call an MCP tool via mcpd's REST API.
    
    Args:
        server: MCP server name
        tool: Tool name to call
        args: Arguments for the tool
        mcpd_url: Base URL for mcpd
        headers: Optional headers (for future AGNTCY DID auth)
    """
    try:
        # Future: AGNTCY headers would be added here
        # headers = headers or {}
        # if agntcy_did := os.getenv("AGNTCY_DID"):
        #     headers["X-AGNTCY-DID"] = agntcy_did
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{mcpd_url}/api/v1/servers/{server}/tools/{tool}",
                json=args,
                headers=headers,
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
            
            # mcpd returns the extracted message in the "body" field
            if isinstance(result, dict) and "body" in result:
                return result["body"]
            # Fallback for direct string responses
            return str(result)
    except Exception as e:
        return f"Error calling MCP tool {tool}: {e!s}"


def create_mcpd_tool(
    server: str, 
    tool_name: str, 
    mcpd_url: str = "http://localhost:8090"
):
    """Create a tool function that calls mcpd.
    
    This demonstrates the pattern used in agent-factory
    for creating callable tool functions.
    """
    async def tool_func(**kwargs) -> str:
        return await mcpd_call_tool(server, tool_name, kwargs, mcpd_url)
    
    tool_func.__name__ = tool_name
    tool_func.__doc__ = f"Call {tool_name} via mcpd server {server}"
    tool_func.__annotations__ = {"return": str}
    
    return tool_func


# Example: Create filesystem tools
def create_filesystem_tools(mcpd_url: str = "http://localhost:8090") -> List:
    """Create filesystem tools that work with mcpd.
    
    This shows the migration path from:
    - MCPStdio (subprocess-based)
    - To: mcpd REST API (HTTP-based)
    """
    tools = []
    
    # Create read_file tool
    read_file = create_mcpd_tool("filesystem", "read_file", mcpd_url)
    read_file.__doc__ = "Read the contents of a file at the specified path"
    read_file.__annotations__["path"] = str
    tools.append(read_file)
    
    # Create list_directory tool
    list_directory = create_mcpd_tool("filesystem", "list_directory", mcpd_url)
    list_directory.__doc__ = "List the contents of a directory"
    list_directory.__annotations__["path"] = str
    tools.append(list_directory)
    
    return tools