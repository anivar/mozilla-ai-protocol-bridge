#!/usr/bin/env python3
"""Advanced MCP-ACP Bridge Demo

Shows enterprise features:
1. AGNTCY Identity integration
2. Multiple tool support
3. Enterprise authentication patterns
"""

import asyncio
import sys
sys.path.append('..')

from bridge.config_acp import MCPToACPBridgeConfig
from bridge.server_acp import serve_mcp_as_acp_async


async def main():
    print("🚀 Advanced MCP-ACP Bridge Demo")
    print("=" * 45)
    
    # Enterprise bridge configuration
    bridge_config = MCPToACPBridgeConfig(
        mcp_command="echo",
        mcp_args=["Enterprise MCP Server"],
        host="localhost", 
        port=8091,
        endpoint="/enterprise-bridge",
        server_name="enterprise-tools",
        organization="mozilla-ai-demo",
        identity_id="did:agntcy:dev:mozilla-ai-demo:enterprise-tools",
        version="1.0.0"
    )
    
    print(f"🔐 Starting enterprise bridge with identity:")
    print(f"   Identity: {bridge_config.identity_id}")
    print(f"   Org: {bridge_config.organization}")
    print(f"   URL: http://{bridge_config.host}:{bridge_config.port}{bridge_config.endpoint}")
    
    # Start the bridge server
    server_handle = await serve_mcp_as_acp_async(bridge_config)
    
    # Give server time to start
    await asyncio.sleep(1)
    
    print("\n✅ Enterprise bridge is running!")
    
    print("\n🔍 Try these enterprise API calls:")
    
    print("\n1. Get agent manifest (with identity):")
    print(f'   curl -H "X-AGNTCY-Identity: {bridge_config.identity_id}" \\')
    print(f'        -H "X-AGNTCY-Organization: {bridge_config.organization}" \\')
    print(f'        http://localhost:8091/enterprise-bridge/agents')
    
    print("\n2. Execute tool with enterprise context:")
    print(f'   curl -X POST http://localhost:8091/enterprise-bridge/runs/stateless \\')
    print(f'     -H "Content-Type: application/json" \\')
    print(f'     -H "X-AGNTCY-Identity: {bridge_config.identity_id}" \\')
    print(f'     -d \'{{"config": {{"tool": "echo", "args": {{"message": "Enterprise Hello!"}}}}, "metadata": {{"identity_id": "{bridge_config.identity_id}"}}}}\'')
    
    print("\n3. Search agents:")
    print(f'   curl -X POST http://localhost:8091/enterprise-bridge/agents/search \\')
    print(f'     -H "Content-Type: application/json" \\')
    print(f'     -d \'{{}}\'')
    
    print("\n⚡ Enterprise features demonstrated:")
    print("   • W3C DID identity integration")
    print("   • Enterprise authentication headers")
    print("   • Organization-based access control") 
    print("   • Metadata-rich tool execution")
    print("   • Standards-compliant ACP API")
    
    print("\n💼 Use case: Corporate MCP tools accessible via standard REST API")
    print("   with enterprise identity verification and audit trails")
    
    print(f"\n🎯 Enterprise Bridge URL: http://localhost:8091/enterprise-bridge")
    print("   Press Ctrl+C to stop")
    
    try:
        # Keep server running
        await server_handle.task
    except KeyboardInterrupt:
        print("\n👋 Shutting down enterprise bridge...")
        await server_handle.shutdown()


if __name__ == "__main__":
    asyncio.run(main())