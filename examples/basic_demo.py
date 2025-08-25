#!/usr/bin/env python3
"""Basic MCP-ACP Bridge Demo

Shows how to:
1. Start a simple MCP server as an ACP service  
2. Query the ACP API
3. Execute tools through REST
"""

import asyncio
import sys
sys.path.append('..')

from bridge.config_acp import MCPToACPBridgeConfig
from bridge.server_acp import serve_mcp_as_acp_async


async def main():
    print("🚀 MCP-ACP Bridge Demo")
    print("=" * 40)
    
    # Configure the bridge
    bridge_config = MCPToACPBridgeConfig(
        mcp_command="echo",  # Simple echo command for demo
        mcp_args=["MCP server simulator"],
        host="localhost",
        port=8090,
        endpoint="/mcp-bridge",
        server_name="demo-server",
        organization="demo-org"
    )
    
    print(f"📡 Starting bridge at http://{bridge_config.host}:{bridge_config.port}{bridge_config.endpoint}")
    
    # Start the bridge server
    server_handle = await serve_mcp_as_acp_async(bridge_config)
    
    # Give server time to start
    await asyncio.sleep(1)
    
    print("\n✅ Bridge is running!")
    print("\n📋 Try these commands in another terminal:")
    print(f"   curl http://localhost:8090/mcp-bridge/agents")
    print(f'   curl -X POST http://localhost:8090/mcp-bridge/runs/stateless \\')
    print(f'     -H "Content-Type: application/json" \\')
    print(f'     -d \'{{"config": {{"tool": "echo", "args": {{"message": "Hello Bridge!"}}}}}}\'')
    
    print("\n⚡ Features demonstrated:")
    print("   • MCP server → ACP REST API translation")
    print("   • Tool discovery and execution")
    print("   • Async architecture")
    print("   • Standard ACP endpoints")
    
    print(f"\n🎯 Bridge URL: http://localhost:8090/mcp-bridge")
    print("   Press Ctrl+C to stop")
    
    try:
        # Keep server running
        await server_handle.task
    except KeyboardInterrupt:
        print("\n👋 Shutting down bridge...")
        await server_handle.shutdown()


if __name__ == "__main__":
    asyncio.run(main())