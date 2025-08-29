"""Demo showing httpx client features in the bridge.

This demonstrates advanced HTTP features that were rejected in PR mozilla-ai/any-llm#254
but are now available in the protocol bridges.
"""

import asyncio
import httpx
from bridge.config_acp import MCPToACPBridgeConfig
from bridge.server_acp import serve_mcp_as_acp_async


async def main():
    """Run bridge with custom httpx client showing rejected features."""
    
    # Create custom httpx client with features from rejected PR
    custom_http_client = httpx.AsyncClient(
        # Connection pooling for performance
        limits=httpx.Limits(
            max_keepalive_connections=20,  # Reuse connections
            max_connections=50,            # Total connection limit
            keepalive_expiry=60.0,        # Keep connections alive
        ),
        
        # Custom headers for tracking and auth
        headers={
            "User-Agent": "MCP-ACP-Bridge/1.0 (Rejected-Features-Demo)",
            "X-Bridge-Version": "1.0.0",
            "X-Feature-Origin": "any-llm-pr-254-rejected",
        },
        
        # Timeout configuration
        timeout=httpx.Timeout(
            connect=10.0,   # Connection timeout
            read=60.0,      # Read timeout for slow tools
            write=20.0,     # Write timeout
            pool=10.0,      # Pool timeout
        ),
        
        # Enable HTTP/2 for multiplexing
        http2=True,
        
        # Follow redirects
        follow_redirects=True,
        
        # Retry transport for reliability
        transport=httpx.AsyncHTTPTransport(
            retries=3,
            http2=True,
        ),
    )
    
    # Configure bridge with the custom client
    config = MCPToACPBridgeConfig(
        mcp_command="uvx",
        mcp_args=["mcp-server-time"],  # Simple example server
        http_client=custom_http_client,  # Pass the rejected feature
        port=8091,
        identity_id="did:agntcy:demo:httpx-features",
        organization="rejected-features-demo"
    )
    
    try:
        # Start the bridge
        server_handle = await serve_mcp_as_acp_async(config)
        
        print("🚀 Bridge running with rejected httpx features:")
        print(f"   URL: http://localhost:{config.port}")
        print(f"   Features from rejected PR #254:")
        print(f"   - Connection pooling: {custom_http_client._limits.max_connections} connections")
        print(f"   - HTTP/2 enabled: True")
        print(f"   - Retry count: 3")
        print(f"   - Custom headers: Yes")
        print(f"   - Identity: {config.identity_id}")
        print()
        print("These performance features were rejected by Mozilla AI")
        print("but are now available in the protocol bridges!")
        
        # Keep running
        await asyncio.Event().wait()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await custom_http_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())