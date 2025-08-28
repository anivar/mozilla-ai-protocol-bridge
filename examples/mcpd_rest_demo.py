#!/usr/bin/env python3
"""Demo showing mcpd REST API integration approach from agent-factory PR #310.

This demonstrates the direct REST API approach to mcpd integration,
as implemented in agent-factory for production use.
"""

import asyncio
import httpx
from typing import Any, Dict


async def mcpd_call_tool(
    server: str, 
    tool: str, 
    args: Dict[str, Any], 
    mcpd_url: str = "http://localhost:8090"
) -> str:
    """Call an MCP tool via mcpd's REST API.
    
    This is the core function from agent-factory's mcpd_tools.py
    that replaces MCPStdio with direct REST calls.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{mcpd_url}/api/v1/servers/{server}/tools/{tool}",
                json=args,
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
            
            # mcpd returns the extracted message in the "body" field
            if isinstance(result, dict) and "body" in result:
                return result["body"]
            return str(result)
    except Exception as e:
        return f"Error calling MCP tool {tool}: {e!s}"


async def demo_filesystem_operations():
    """Demo filesystem operations using mcpd REST API."""
    print("=== mcpd REST API Demo (agent-factory approach) ===\n")
    
    # List directory
    print("1. Listing current directory:")
    result = await mcpd_call_tool(
        server="filesystem",
        tool="list_directory", 
        args={"path": "."}
    )
    print(f"   Result: {result[:200]}...\n")
    
    # Read a file
    print("2. Reading README.md:")
    result = await mcpd_call_tool(
        server="filesystem",
        tool="read_file",
        args={"path": "README.md"}
    )
    print(f"   Result: {result[:200]}...\n")
    
    print("Key Benefits of this approach:")
    print("• No subprocess management - just HTTP")
    print("• Built-in error handling via HTTP status codes") 
    print("• Easy to add identity headers (for AGNTCY)")
    print("• Works with any HTTP client library")
    print("• Production-ready for agent-factory workflows")


async def demo_with_identity():
    """Demo how identity would work with AGNTCY support."""
    print("\n=== With AGNTCY Identity (future) ===\n")
    print("When mcpd PR #154 is merged, you'll be able to:")
    print("")
    print("```python")
    print("headers = {'X-AGNTCY-DID': 'did:agntcy:mcpd:org:server'}")
    print("response = await client.post(url, json=args, headers=headers)")
    print("```")
    print("")
    print("This provides cryptographic verification of tool access!")


async def main():
    """Run all demos."""
    print("\nMCPD REST API Integration Demo")
    print("==============================")
    print("This shows the production approach from agent-factory PR #310")
    print("")
    
    # Check if mcpd is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8090/api/v1/servers")
            if response.status_code == 200:
                print("✓ mcpd is running")
                servers = response.json().get("body", [])
                print(f"  Available servers: {', '.join(servers)}\n")
            else:
                print("✗ mcpd returned unexpected status:", response.status_code)
                return
    except Exception as e:
        print("✗ mcpd is not running at http://localhost:8090")
        print("  Please start mcpd first:")
        print("  $ mcpd run filesystem")
        print(f"  Error: {e}")
        return
    
    # Run demos
    await demo_filesystem_operations()
    await demo_with_identity()


if __name__ == "__main__":
    asyncio.run(main())