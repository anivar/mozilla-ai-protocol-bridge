#!/usr/bin/env python3
"""Demo script for MCP-ACP bridge.

This example shows how to:
1. Start an MCP server (filesystem tools) as an ACP service
2. Query the ACP manifest
3. Execute tools through the ACP interface
"""

import asyncio
import httpx
from pathlib import Path

from any_agent.config import MCPParams, MCPStdio
from any_agent.serving import MCPToACPBridgeConfig, serve_mcp_as_acp_async


async def main():
    print("🚀 MCP-ACP Bridge Demo")
    print("=" * 50)
    
    # Configure MCP server (using filesystem tools as example)
    mcp_config = MCPParams(
        transport=MCPStdio(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        )
    )
    
    # Configure bridge
    bridge_config = MCPToACPBridgeConfig(
        mcp_config=mcp_config,
        host="localhost",
        port=8090,
        endpoint="/mcp-bridge",
        server_name="filesystem-server",
        organization="mozilla-ai-demo",
        version="1.0.0",
        # Optional: Add AGNTCY Identity if available
        # identity_id="did:agntcy:dev:mozilla-ai-demo:filesystem-server"
    )
    
    print(f"📡 Starting MCP-ACP bridge on http://{bridge_config.host}:{bridge_config.port}{bridge_config.endpoint}")
    
    # Start the bridge
    server_handle = await serve_mcp_as_acp_async(
        mcp_config=mcp_config,
        bridge_config=bridge_config,
        framework="tinyagent"
    )
    
    # Give server time to start
    await asyncio.sleep(2)
    
    # Create HTTP client for ACP interactions
    async with httpx.AsyncClient() as client:
        base_url = f"http://{bridge_config.host}:{bridge_config.port}{bridge_config.endpoint}"
        
        # 1. List available agents
        print("\n📋 Listing available agents...")
        response = await client.get(f"{base_url}/agents")
        agents = response.json()
        print(f"Found {len(agents)} agent(s):")
        for agent in agents:
            print(f"  - {agent['name']} (ID: {agent['id']})")
        
        # 2. Get agent manifest
        print("\n📄 Getting agent manifest...")
        agent_id = f"mcp-bridge-{bridge_config.server_name}"
        response = await client.get(f"{base_url}/agents/{agent_id}")
        agent_detail = response.json()
        
        print(f"Agent: {agent_detail['name']}")
        print(f"Description: {agent_detail['description']}")
        print(f"Available tools:")
        for tool in agent_detail['acp_descriptor']['tools']:
            print(f"  - {tool['name']}: {tool['description']}")
        
        # 3. Create a test file
        print("\n✍️  Creating test file...")
        test_content = "Hello from MCP-ACP bridge!"
        run_request = {
            "config": {
                "tool": "write_file",
                "args": {
                    "path": "/tmp/mcp_acp_test.txt",
                    "content": test_content
                }
            }
        }
        
        response = await client.post(f"{base_url}/runs/stateless", json=run_request)
        result = response.json()
        
        if result["status"] == "completed":
            print(f"✅ File created successfully!")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        # 4. Read the file back
        print("\n📖 Reading file back...")
        run_request = {
            "config": {
                "tool": "read_file",
                "args": {
                    "path": "/tmp/mcp_acp_test.txt"
                }
            }
        }
        
        response = await client.post(f"{base_url}/runs/stateless", json=run_request)
        result = response.json()
        
        if result["status"] == "completed":
            content = result["output"]["result"]
            print(f"✅ File content: {content}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        # 5. List directory
        print("\n📁 Listing /tmp directory...")
        run_request = {
            "config": {
                "tool": "list_directory",
                "args": {
                    "path": "/tmp"
                }
            }
        }
        
        response = await client.post(f"{base_url}/runs/stateless", json=run_request)
        result = response.json()
        
        if result["status"] == "completed":
            entries = result["output"]["result"].get("entries", [])
            print(f"Found {len(entries)} items in /tmp")
            # Show first 5 entries
            for entry in entries[:5]:
                print(f"  - {entry['name']} ({'dir' if entry['is_directory'] else 'file'})")
            if len(entries) > 5:
                print(f"  ... and {len(entries) - 5} more")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    print("\n🎉 Demo complete! Press Ctrl+C to stop the bridge.")
    
    # Keep server running
    try:
        await server_handle.task
    except KeyboardInterrupt:
        print("\n👋 Shutting down bridge...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")