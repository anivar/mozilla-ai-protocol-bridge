#!/usr/bin/env python3
"""Advanced MCP-ACP bridge demo with AGNTCY Identity support.

This example shows how to:
1. Use AGNTCY Identity with the bridge
2. Create a custom MCP tool server
3. Handle authentication and identity verification
"""

import asyncio
import httpx
import json
from typing import Dict, Any
from pathlib import Path

from any_agent.config import MCPParams, MCPStdio
from any_agent.serving import MCPToACPBridgeConfig, serve_mcp_as_acp_async


# Mock AGNTCY Identity manager (in real usage, use agntcy-sdk)
class MockIdentityManager:
    """Mock identity manager for demo purposes."""
    
    @staticmethod
    def create_identity(org: str, server_name: str) -> Dict[str, Any]:
        """Create a mock AGNTCY Identity document."""
        did = f"did:agntcy:dev:{org}:{server_name}"
        return {
            "id": did,
            "resolverMetadata": {
                "id": did,
                "assertionMethod": [{
                    "id": f"{did}#key-1",
                    "publicKeyJwk": {
                        "kty": "EC",
                        "crv": "P-256",
                        "x": "mock_x_coordinate",
                        "y": "mock_y_coordinate"
                    }
                }],
                "service": [{
                    "id": f"{did}#mcp",
                    "type": "MCPService",
                    "serviceEndpoint": f"/servers/{server_name}"
                }]
            }
        }


async def demo_with_identity():
    print("🚀 MCP-ACP Bridge Demo with AGNTCY Identity")
    print("=" * 50)
    
    # Create mock identity
    org = "mozilla-ai-demo"
    server_name = "secure-filesystem"
    identity = MockIdentityManager.create_identity(org, server_name)
    
    print(f"🆔 Created identity: {identity['id']}")
    
    # Configure MCP server
    mcp_config = MCPParams(
        transport=MCPStdio(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        )
    )
    
    # Configure bridge with identity
    bridge_config = MCPToACPBridgeConfig(
        mcp_config=mcp_config,
        host="localhost",
        port=8091,
        endpoint="/secure-mcp",
        server_name=server_name,
        organization=org,
        version="1.0.0",
        identity_id=identity['id']
    )
    
    print(f"📡 Starting secure MCP-ACP bridge on http://{bridge_config.host}:{bridge_config.port}{bridge_config.endpoint}")
    
    # Start the bridge
    server_handle = await serve_mcp_as_acp_async(
        mcp_config=mcp_config,
        bridge_config=bridge_config,
        framework="tinyagent"
    )
    
    # Give server time to start
    await asyncio.sleep(2)
    
    # Create HTTP client with auth headers
    async with httpx.AsyncClient() as client:
        base_url = f"http://{bridge_config.host}:{bridge_config.port}{bridge_config.endpoint}"
        
        # In a real scenario, you would sign requests with your identity
        headers = {
            "X-AGNTCY-Identity": identity['id'],
            "X-AGNTCY-Organization": org
        }
        
        # 1. Get agent with identity info
        print("\n📄 Getting agent manifest with identity...")
        agent_id = f"mcp-bridge-{bridge_config.server_name}"
        response = await client.get(f"{base_url}/agents/{agent_id}", headers=headers)
        agent_detail = response.json()
        
        print(f"Agent: {agent_detail['name']}")
        print(f"Organization: {agent_detail['metadata']['organization']}")
        print(f"Identity ID: {agent_detail.get('metadata', {}).get('identity_id', 'Not set')}")
        
        # 2. Execute secure operation
        print("\n🔐 Executing secure file operation...")
        run_request = {
            "config": {
                "tool": "write_file",
                "args": {
                    "path": "/tmp/secure_data.json",
                    "content": json.dumps({
                        "message": "Secure data from MCP-ACP bridge",
                        "identity": identity['id'],
                        "timestamp": "2025-08-25T10:00:00Z"
                    }, indent=2)
                }
            },
            "metadata": {
                "identity_id": identity['id'],
                "signed": True  # In real usage, include actual signature
            }
        }
        
        response = await client.post(
            f"{base_url}/runs/stateless", 
            json=run_request,
            headers=headers
        )
        result = response.json()
        
        if result["status"] == "completed":
            print(f"✅ Secure file created successfully!")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
        
        # 3. Verify secure data
        print("\n🔍 Verifying secure data...")
        run_request = {
            "config": {
                "tool": "read_file",
                "args": {
                    "path": "/tmp/secure_data.json"
                }
            }
        }
        
        response = await client.post(
            f"{base_url}/runs/stateless", 
            json=run_request,
            headers=headers
        )
        result = response.json()
        
        if result["status"] == "completed":
            content = json.loads(result["output"]["result"])
            print(f"✅ Verified data:")
            print(f"   Message: {content['message']}")
            print(f"   Identity: {content['identity']}")
            print(f"   Timestamp: {content['timestamp']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    print("\n🎉 Secure demo complete! Press Ctrl+C to stop the bridge.")
    
    # Keep server running
    try:
        await server_handle.task
    except KeyboardInterrupt:
        print("\n👋 Shutting down secure bridge...")


async def demo_multi_bridge():
    """Demo running multiple MCP servers as ACP services."""
    print("🚀 Multi-Bridge Demo: MCP + A2A + ACP")
    print("=" * 50)
    
    # Start multiple bridges
    bridges = []
    
    # 1. Filesystem MCP as ACP
    fs_config = MCPParams(
        transport=MCPStdio(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
        )
    )
    fs_bridge = MCPToACPBridgeConfig(
        mcp_config=fs_config,
        host="localhost",
        port=8092,
        endpoint="/fs",
        server_name="filesystem"
    )
    
    print("📁 Starting filesystem MCP-ACP bridge...")
    fs_handle = await serve_mcp_as_acp_async(fs_config, fs_bridge)
    bridges.append(("Filesystem", fs_bridge, fs_handle))
    
    # 2. Git MCP as ACP (if available)
    try:
        git_config = MCPParams(
            transport=MCPStdio(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-git", "."]
            )
        )
        git_bridge = MCPToACPBridgeConfig(
            mcp_config=git_config,
            host="localhost",
            port=8093,
            endpoint="/git",
            server_name="git"
        )
        
        print("🔀 Starting git MCP-ACP bridge...")
        git_handle = await serve_mcp_as_acp_async(git_config, git_bridge)
        bridges.append(("Git", git_bridge, git_handle))
    except Exception as e:
        print(f"⚠️  Could not start git bridge: {e}")
    
    # Give servers time to start
    await asyncio.sleep(2)
    
    # Query all bridges
    print("\n📋 Available ACP services:")
    async with httpx.AsyncClient() as client:
        for name, config, _ in bridges:
            base_url = f"http://{config.host}:{config.port}{config.endpoint}"
            try:
                response = await client.get(f"{base_url}/agents")
                agents = response.json()
                print(f"\n{name} Bridge ({base_url}):")
                for agent in agents:
                    print(f"  - {agent['name']}")
                    tools = agent.get('acp_descriptor', {}).get('tools', [])
                    print(f"    Tools: {', '.join(t['name'] for t in tools[:3])}...")
            except Exception as e:
                print(f"  ❌ Error querying {name}: {e}")
    
    print("\n🎉 All bridges running! Press Ctrl+C to stop.")
    
    # Keep servers running
    try:
        await asyncio.gather(*[h.task for _, _, h in bridges])
    except KeyboardInterrupt:
        print("\n👋 Shutting down all bridges...")


async def main():
    """Run demo based on command line selection."""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "identity":
        await demo_with_identity()
    elif len(sys.argv) > 1 and sys.argv[1] == "multi":
        await demo_multi_bridge()
    else:
        print("Usage:")
        print("  python mcp_acp_bridge_with_identity.py          # Run basic demo")
        print("  python mcp_acp_bridge_with_identity.py identity # Run with AGNTCY Identity")
        print("  python mcp_acp_bridge_with_identity.py multi    # Run multiple bridges")
        print("\nRunning basic demo with identity...")
        await demo_with_identity()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")