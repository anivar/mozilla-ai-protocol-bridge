"""ACP server implementation for MCP-ACP bridge."""

import asyncio
from typing import Optional

from any_agent.logging import logger
from any_agent.serving.server_handle import ServerHandle

from .bridge_executor import MCPToACPBridgeExecutor
from .config_acp import MCPToACPBridgeConfig

# Check if ACP is available
acp_available = False
try:
    from agntcy_acp import (
        Agent,
        AgentMetadata,
        RunCreateStateless,
    )
    acp_available = True
except ImportError:
    pass


async def serve_mcp_as_acp_async(
    mcp_config,
    bridge_config: Optional[MCPToACPBridgeConfig] = None,
    framework: str = "tinyagent",
) -> ServerHandle:
    """Serve an MCP server as an ACP service.

    Args:
        mcp_config: MCP server configuration
        bridge_config: Bridge configuration (uses defaults if not provided)
        framework: Agent framework to use for tool conversion

    Returns:
        ServerHandle for managing the server

    Raises:
        ImportError: If ACP dependencies are not installed
    """
    if not acp_available:
        msg = "You need to `pip install 'agntcy-acp'` to use MCP to ACP bridge"
        raise ImportError(msg)
    
    from any_agent.config import AgentFramework
    from any_agent.tools.mcp.mcp_client import MCPClient
    import uvicorn
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import JSONResponse
    
    # Use default config if not provided
    if bridge_config is None:
        bridge_config = MCPToACPBridgeConfig(mcp_config=mcp_config)
    else:
        # Ensure mcp_config is set
        bridge_config.mcp_config = mcp_config
    
    # Create and connect MCP client
    mcp_client = MCPClient(
        config=mcp_config,
        framework=AgentFramework.from_string(framework),
    )
    await mcp_client.connect()
    
    # Create executor
    executor = MCPToACPBridgeExecutor(mcp_client, bridge_config)
    await executor.initialize()
    
    # Create route handlers
    route_handlers = _create_route_handlers(executor, bridge_config)
    
    # Create Starlette app with ACP routes
    app = _create_starlette_app(bridge_config, route_handlers)
    
    # Create and start server
    server_handle = await _start_uvicorn_server(app, bridge_config)
    
    # Log startup information
    _log_server_startup(bridge_config, server_handle)
    
    return server_handle


def _create_route_handlers(executor: MCPToACPBridgeExecutor, bridge_config: MCPToACPBridgeConfig):
    """Create ACP route handlers."""
    
    async def get_agents(request):
        """List available agents (in this case, just our bridge)."""
        agent = _create_agent_response(executor, bridge_config)
        return JSONResponse([agent.model_dump() if hasattr(agent, 'model_dump') else agent])
    
    async def search_agents(request):
        """Search agents - returns our bridge if it matches."""
        # For simplicity, always return our agent
        return await get_agents(request)
    
    async def get_agent_by_id(request):
        """Get specific agent by ID."""
        agent_id = request.path_params["agent_id"]
        expected_id = f"mcp-bridge-{bridge_config.server_name}"
        
        if agent_id != expected_id:
            return JSONResponse({"error": "Agent not found"}, status_code=404)
        
        agent = _create_agent_response(executor, bridge_config)
        return JSONResponse(agent.model_dump() if hasattr(agent, 'model_dump') else agent)
    
    async def create_stateless_run(request):
        """Create a stateless run."""
        body = await request.json()
        
        if acp_available:
            run_request = RunCreateStateless(**body)
        else:
            # Fallback when ACP not available
            run_request = type('RunRequest', (), body)
        
        # Execute the run
        result = await executor.execute_stateless_run(run_request)
        
        result_dict = result.model_dump() if hasattr(result, 'model_dump') else result
        return JSONResponse(result_dict)
    
    async def get_stateless_run(request):
        """Get stateless run status - not implemented for bridge."""
        return JSONResponse(
            {"error": "Run history not supported in bridge mode"}, 
            status_code=501
        )
    
    return {
        "get_agents": get_agents,
        "search_agents": search_agents,
        "get_agent_by_id": get_agent_by_id,
        "create_stateless_run": create_stateless_run,
        "get_stateless_run": get_stateless_run,
    }


def _create_agent_response(executor: MCPToACPBridgeExecutor, bridge_config: MCPToACPBridgeConfig):
    """Create agent response object."""
    agent_id = f"mcp-bridge-{bridge_config.server_name}"
    agent_name = f"{bridge_config.server_name} MCP Bridge"
    agent_description = f"MCP server '{bridge_config.server_name}' exposed via ACP"
    
    if acp_available:
        return Agent(
            id=agent_id,
            name=agent_name,
            description=agent_description,
            metadata=AgentMetadata(
                organization=bridge_config.organization,
                version=bridge_config.version,
            ),
            acp_descriptor=executor._agent_manifest.get("acp", {}),
        )
    else:
        # Fallback when ACP not available
        return {
            "id": agent_id,
            "name": agent_name,
            "description": agent_description,
            "metadata": {
                "organization": bridge_config.organization,
                "version": bridge_config.version,
            },
            "acp_descriptor": executor._agent_manifest.get("acp", {}),
        }


def _create_starlette_app(bridge_config: MCPToACPBridgeConfig, handlers: dict) -> "Starlette":
    """Create Starlette app with ACP routes."""
    from starlette.applications import Starlette
    from starlette.routing import Route
    
    base_path = bridge_config.endpoint.rstrip("/")
    routes = [
        Route(f"{base_path}/agents/search", handlers["search_agents"], methods=["POST"]),
        Route(f"{base_path}/agents", handlers["get_agents"], methods=["GET"]),
        Route(f"{base_path}/agents/{{agent_id}}", handlers["get_agent_by_id"], methods=["GET"]),
        Route(f"{base_path}/runs/stateless", handlers["create_stateless_run"], methods=["POST"]),
        Route(f"{base_path}/runs/stateless/{{run_id}}", handlers["get_stateless_run"], methods=["GET"]),
    ]
    
    return Starlette(routes=routes)


async def _start_uvicorn_server(app, bridge_config: MCPToACPBridgeConfig) -> ServerHandle:
    """Start uvicorn server and return handle."""
    import uvicorn
    
    # Create and start server
    config = uvicorn.Config(
        app,
        host=bridge_config.host,
        port=bridge_config.port,
        log_level=bridge_config.log_level,
    )
    server = uvicorn.Server(config)
    
    # Start server in background
    task = asyncio.create_task(server.serve())
    
    # Wait for server to start
    while not server.started:
        await asyncio.sleep(0.1)
    
    return ServerHandle(task=task, server=server)


def _log_server_startup(bridge_config: MCPToACPBridgeConfig, server_handle: ServerHandle) -> None:
    """Log server startup information."""
    # Get actual port if using dynamic port
    actual_port = bridge_config.port
    if bridge_config.port == 0 and hasattr(server_handle.server, 'servers') and server_handle.server.servers:
        actual_port = server_handle.server.servers[0].sockets[0].getsockname()[1]
    
    bridge_url = f"http://{bridge_config.host}:{actual_port}{bridge_config.endpoint}"
    
    if bridge_config.identity_id:
        logger.info(f"MCP to ACP bridge started at {bridge_url} with identity {bridge_config.identity_id}")
    else:
        logger.info(f"MCP to ACP bridge started at {bridge_url}")
    
    logger.info(f"ACP manifest available at: {bridge_url}/agents")