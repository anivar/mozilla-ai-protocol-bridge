"""Tests for MCP-ACP bridge functionality."""

import asyncio
import json
from typing import Any, Dict

import httpx
import pytest

from any_agent.config import MCPParams, MCPStdio
from any_agent.serving import MCPToACPBridgeConfig, serve_mcp_as_acp_async
from any_agent.testing.helpers import wait_for_server_async


# Skip if ACP not available
acp_available = True
try:
    from agntcy_acp import RunCreateStateless, RunStatus
except ImportError:
    acp_available = False


@pytest.fixture
def mock_mcp_config() -> MCPParams:
    """Create a mock MCP configuration for testing."""
    # Use echo server for predictable testing
    return MCPParams(
        transport=MCPStdio(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-everything", "--test-mode"]
        )
    )


@pytest.mark.asyncio
@pytest.mark.skipif(not acp_available, reason="ACP SDK not installed")
async def test_mcp_acp_bridge_basic(mock_mcp_config: MCPParams, test_port: int) -> None:
    """Test basic MCP-ACP bridge functionality."""
    bridge_config = MCPToACPBridgeConfig(
        mcp_config=mock_mcp_config,
        host="localhost",
        port=test_port,
        endpoint="/mcp-bridge",
        server_name="test-server",
        organization="test-org",
        version="1.0.0"
    )
    
    server_handle = await serve_mcp_as_acp_async(
        mcp_config=mock_mcp_config,
        bridge_config=bridge_config,
        framework="tinyagent"
    )
    
    try:
        # Wait for server to start
        base_url = f"http://localhost:{test_port}/mcp-bridge"
        await wait_for_server_async(f"http://localhost:{test_port}")
        
        async with httpx.AsyncClient() as client:
            # Test agent listing
            response = await client.get(f"{base_url}/agents")
            assert response.status_code == 200
            agents = response.json()
            assert len(agents) == 1
            assert agents[0]["id"] == "mcp-bridge-test-server"
            assert agents[0]["name"] == "test-server MCP Bridge"
            
            # Test agent details
            agent_id = agents[0]["id"]
            response = await client.get(f"{base_url}/agents/{agent_id}")
            assert response.status_code == 200
            agent_detail = response.json()
            assert agent_detail["id"] == agent_id
            assert "acp_descriptor" in agent_detail
            assert agent_detail["acp_descriptor"]["capabilities"]["stateless"] is True
            assert agent_detail["acp_descriptor"]["capabilities"]["stateful"] is False
            
    finally:
        if server_handle:
            await server_handle.shutdown()


@pytest.mark.asyncio
@pytest.mark.skipif(not acp_available, reason="ACP SDK not installed")
async def test_mcp_acp_bridge_with_identity(mock_mcp_config: MCPParams, test_port: int) -> None:
    """Test MCP-ACP bridge with AGNTCY Identity."""
    identity_id = "did:agntcy:dev:test-org:test-server"
    
    bridge_config = MCPToACPBridgeConfig(
        mcp_config=mock_mcp_config,
        host="localhost",
        port=test_port,
        endpoint="/secure-mcp",
        server_name="test-server",
        organization="test-org",
        version="1.0.0",
        identity_id=identity_id
    )
    
    server_handle = await serve_mcp_as_acp_async(
        mcp_config=mock_mcp_config,
        bridge_config=bridge_config,
        framework="tinyagent"
    )
    
    try:
        # Wait for server to start
        base_url = f"http://localhost:{test_port}/secure-mcp"
        await wait_for_server_async(f"http://localhost:{test_port}")
        
        async with httpx.AsyncClient() as client:
            # Test with identity headers
            headers = {
                "X-AGNTCY-Identity": identity_id,
                "X-AGNTCY-Organization": "test-org"
            }
            
            response = await client.get(f"{base_url}/agents", headers=headers)
            assert response.status_code == 200
            agents = response.json()
            assert len(agents) == 1
            
            # Verify identity in metadata
            agent_id = agents[0]["id"]
            response = await client.get(f"{base_url}/agents/{agent_id}", headers=headers)
            assert response.status_code == 200
            agent_detail = response.json()
            assert agent_detail["metadata"]["organization"] == "test-org"
            # Identity should be in manifest metadata
            assert "identity_id" in str(agent_detail)
            
    finally:
        if server_handle:
            await server_handle.shutdown()


@pytest.mark.asyncio
@pytest.mark.skipif(not acp_available, reason="ACP SDK not installed")
async def test_mcp_acp_bridge_tool_execution(mock_mcp_config: MCPParams, test_port: int) -> None:
    """Test tool execution through MCP-ACP bridge."""
    bridge_config = MCPToACPBridgeConfig(
        mcp_config=mock_mcp_config,
        host="localhost",
        port=test_port,
        endpoint="/mcp-bridge",
        server_name="test-server"
    )
    
    server_handle = await serve_mcp_as_acp_async(
        mcp_config=mock_mcp_config,
        bridge_config=bridge_config,
        framework="tinyagent"
    )
    
    try:
        # Wait for server to start
        base_url = f"http://localhost:{test_port}/mcp-bridge"
        await wait_for_server_async(f"http://localhost:{test_port}")
        
        async with httpx.AsyncClient() as client:
            # Create a stateless run
            run_request = {
                "config": {
                    "tool": "echo",
                    "args": {
                        "message": "Hello from MCP-ACP bridge!"
                    }
                }
            }
            
            response = await client.post(f"{base_url}/runs/stateless", json=run_request)
            assert response.status_code == 200
            result = response.json()
            
            assert result["status"] == "completed"
            assert "output" in result
            assert result["output"]["success"] is True
            assert "result" in result["output"]
            
    finally:
        if server_handle:
            await server_handle.shutdown()


@pytest.mark.asyncio
@pytest.mark.skipif(not acp_available, reason="ACP SDK not installed")
async def test_mcp_acp_bridge_error_handling(mock_mcp_config: MCPParams, test_port: int) -> None:
    """Test error handling in MCP-ACP bridge."""
    bridge_config = MCPToACPBridgeConfig(
        mcp_config=mock_mcp_config,
        host="localhost",
        port=test_port,
        endpoint="/mcp-bridge",
        server_name="test-server"
    )
    
    server_handle = await serve_mcp_as_acp_async(
        mcp_config=mock_mcp_config,
        bridge_config=bridge_config,
        framework="tinyagent"
    )
    
    try:
        # Wait for server to start
        base_url = f"http://localhost:{test_port}/mcp-bridge"
        await wait_for_server_async(f"http://localhost:{test_port}")
        
        async with httpx.AsyncClient() as client:
            # Test unknown tool
            run_request = {
                "config": {
                    "tool": "unknown_tool",
                    "args": {}
                }
            }
            
            response = await client.post(f"{base_url}/runs/stateless", json=run_request)
            assert response.status_code == 200
            result = response.json()
            
            assert result["status"] == "failed"
            assert "error" in result
            assert "Unknown tool" in result["error"]["message"]
            
            # Test missing tool when multiple available
            run_request = {
                "config": {
                    "args": {"some": "data"}
                }
            }
            
            response = await client.post(f"{base_url}/runs/stateless", json=run_request)
            assert response.status_code == 200
            result = response.json()
            
            # Should fail because multiple tools and none specified
            assert result["status"] == "failed"
            assert "error" in result
            
    finally:
        if server_handle:
            await server_handle.shutdown()


@pytest.mark.asyncio
@pytest.mark.skipif(not acp_available, reason="ACP SDK not installed")
async def test_mcp_acp_bridge_search_agents(mock_mcp_config: MCPParams, test_port: int) -> None:
    """Test agent search functionality."""
    bridge_config = MCPToACPBridgeConfig(
        mcp_config=mock_mcp_config,
        host="localhost", 
        port=test_port,
        endpoint="/mcp-bridge",
        server_name="searchable-server"
    )
    
    server_handle = await serve_mcp_as_acp_async(
        mcp_config=mock_mcp_config,
        bridge_config=bridge_config,
        framework="tinyagent"
    )
    
    try:
        # Wait for server to start
        base_url = f"http://localhost:{test_port}/mcp-bridge"
        await wait_for_server_async(f"http://localhost:{test_port}")
        
        async with httpx.AsyncClient() as client:
            # Search agents (should return our bridge)
            response = await client.post(f"{base_url}/agents/search", json={})
            assert response.status_code == 200
            agents = response.json()
            assert len(agents) == 1
            assert agents[0]["id"] == "mcp-bridge-searchable-server"
            
    finally:
        if server_handle:
            await server_handle.shutdown()


@pytest.mark.asyncio
async def test_mcp_acp_bridge_missing_dependencies() -> None:
    """Test proper error when ACP dependencies are missing."""
    # Temporarily make ACP unavailable
    import sys
    original_modules = {}
    acp_modules = ["agntcy_acp"]
    
    for module in acp_modules:
        if module in sys.modules:
            original_modules[module] = sys.modules[module]
            del sys.modules[module]
    
    try:
        # Force reload
        import importlib
        import any_agent.serving.mcp_acp_bridge
        importlib.reload(any_agent.serving.mcp_acp_bridge)
        
        from any_agent.serving.mcp_acp_bridge import serve_mcp_as_acp_async
        
        mock_config = MCPParams(
            transport=MCPStdio(command="echo", args=["test"])
        )
        
        with pytest.raises(ImportError) as exc_info:
            await serve_mcp_as_acp_async(mock_config)
        
        assert "agntcy-acp" in str(exc_info.value)
        
    finally:
        # Restore original modules
        for module, orig in original_modules.items():
            sys.modules[module] = orig