#!/usr/bin/env python3
"""Demo showing the migration from MCPStdio to mcpd REST API.

This demonstrates the before/after of agent-factory PR #310.
"""

import asyncio
from bridge.mcpd_tools import create_filesystem_tools


def show_old_approach():
    """Show the old MCPStdio approach (for comparison)."""
    print("=== OLD: MCPStdio Approach ===\n")
    print("```python")
    print("from any_agent.config import MCPStdio")
    print("")
    print("# Problems with this approach:")
    print("# - Subprocess management is fragile")
    print("# - No built-in error handling")
    print("# - No identity support")
    print("# - Docker dependency")
    print("")
    print("tools = [")
    print('    MCPStdio(')
    print('        command="docker",')
    print('        args=["run", "-i", "--rm", "mcp/filesystem"],')
    print('        env={"WORKSPACE": "/data"},')
    print('        tools=["read_file", "list_directory"]')
    print('    )')
    print(']')
    print("```\n")


async def show_new_approach():
    """Show the new mcpd REST approach."""
    print("=== NEW: mcpd REST API Approach ===\n")
    print("```python")
    print("from bridge.mcpd_tools import create_filesystem_tools")
    print("")
    print("# Benefits of this approach:")
    print("# - HTTP-based (reliable)")
    print("# - Built-in error handling")
    print("# - Identity support ready")
    print("# - No Docker required")
    print("")
    print("filesystem_tools = create_filesystem_tools(mcpd_url)")
    print("tools = [*filesystem_tools]")
    print("```\n")
    
    # Actually create the tools
    tools = create_filesystem_tools()
    print("Created tools:")
    for tool in tools:
        print(f"  - {tool.__name__}: {tool.__doc__}")
        print(f"    Annotations: {tool.__annotations__}")


async def demonstrate_usage():
    """Show how to use the new tools."""
    print("\n=== Using the New Tools ===\n")
    
    # Create tools
    tools = create_filesystem_tools()
    read_file = tools[0]
    list_directory = tools[1]
    
    print("Example: List directory")
    print("```python")
    print("result = await list_directory(path='.')")
    print("```")
    
    # Try to actually run it
    try:
        result = await list_directory(path=".")
        print(f"\nActual result: {result[:100]}...")
    except Exception as e:
        print(f"\nNote: mcpd not running, would get: {e}")
    
    print("\n\nExample: Read file")
    print("```python") 
    print("content = await read_file(path='README.md')")
    print("```")


async def show_identity_future():
    """Show future identity support."""
    print("\n=== Future: With AGNTCY Identity ===\n")
    print("When mcpd PR #154 is merged:")
    print("")
    print("```python")
    print("# Automatic DID header injection")
    print("os.environ['AGNTCY_DID'] = 'did:agntcy:mcpd:org:server'")
    print("")
    print("# Tools automatically include identity in requests")
    print("result = await read_file(path='sensitive.txt')")
    print("# mcpd verifies the DID signature before allowing access")
    print("```")


async def main():
    """Run the migration demo."""
    print("\nMCPStdio → mcpd Migration Demo")
    print("==============================")
    print("Showing the approach from agent-factory PR #310\n")
    
    show_old_approach()
    await show_new_approach()
    await demonstrate_usage()
    await show_identity_future()
    
    print("\n\nKey Takeaways:")
    print("1. Simpler: No subprocess/Docker management")
    print("2. Reliable: HTTP status codes and retries")
    print("3. Future-proof: Ready for AGNTCY identity")
    print("4. Production-ready: Used in agent-factory")


if __name__ == "__main__":
    asyncio.run(main())