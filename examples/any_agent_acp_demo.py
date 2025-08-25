#!/usr/bin/env python3
"""Demo: Serving any-agent via ACP (Agent Connect Protocol).

This demonstrates how to serve any any-agent framework (tinyagent, langchain, etc.)
via the Linux Foundation's Agent Connect Protocol.

Following patterns from any-agent's existing serving examples.
"""

import asyncio
import sys
sys.path.insert(0, 'src')

from any_agent import AgentConfig, AnyAgent
from any_agent.serving.acp import ACPServingConfig, serve_acp_async


async def main():
    print("🚀 Any-Agent ACP Serving Demo")
    print("=" * 40)
    
    # Create an agent using any framework
    agent_config = AgentConfig(
        name="demo-agent",
        description="Demo agent served via Linux Foundation ACP",
        model_id="anthropic/claude-3-haiku-20240307",  # Using any-llm pattern
        instructions="You are a helpful assistant. Use available tools when needed.",
        tools=[],  # Add your tools here
    )
    
    # Create agent (using tinyagent as example)
    print("📦 Creating any-agent (tinyagent framework)...")
    agent = await AnyAgent.create_async(
        agent_framework="tinyagent",
        agent_config=agent_config,
    )
    
    # Configure ACP serving
    serving_config = ACPServingConfig(
        host="localhost",
        port=8090,
        endpoint="/acp",
        server_name="demo-agent",
        organization="any-agent-demo",
        # Optional: Add W3C DID for enterprise auth
        # identity_id="did:agntcy:dev:any-agent-demo:demo-agent",
    )
    
    print(f"\n📡 Starting ACP server at http://{serving_config.host}:{serving_config.port}{serving_config.endpoint}")
    
    # Start serving via ACP
    server_handle = await serve_acp_async(agent, serving_config)
    
    print("\n✅ Agent is now available via ACP!")
    print("\n📋 Try these commands:")
    print(f"   curl http://localhost:8090/acp/agents")
    print(f'   curl -X POST http://localhost:8090/acp/runs/stateless \\')
    print(f'     -H "Content-Type: application/json" \\')
    print(f'     -d \'{{"input": {{"query": "Hello, what can you help me with?"}}}}\'')
    
    print("\n⚡ Features:")
    print("   • Any-agent framework served via ACP")
    print("   • Linux Foundation standards compliance")
    print("   • W3C DID authentication ready")
    print("   • Async architecture (any-llm patterns)")
    
    print(f"\n🎯 ACP Endpoint: http://localhost:8090/acp")
    print("   Press Ctrl+C to stop")
    
    try:
        await server_handle.task
    except KeyboardInterrupt:
        print("\n👋 Shutting down ACP server...")
        await server_handle.shutdown()


if __name__ == "__main__":
    asyncio.run(main())