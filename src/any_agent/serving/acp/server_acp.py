"""ACP server implementation for any-agent.

Following patterns from any_agent.serving.a2a.server_a2a and any_agent.serving.mcp.server_mcp
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Optional

from any_agent.logging import logger
from any_agent.serving.server_handle import ServerHandle

from .agent_executor import ACPAgentExecutor
from .config_acp import ACPServingConfig

if TYPE_CHECKING:
    from any_agent.frameworks.any_agent import AnyAgent

# Check if ACP is available
acp_available = False
try:
    from agntcy_acp import (
        Agent,
        AgentMetadata,
        RunCreateStateless,
        RunStateless,
        RunStatus,
    )
    acp_available = True
except ImportError:
    # Provide fallback classes when ACP not available
    class RunStatus:
        completed = "completed"
        failed = "failed"
    
    class Agent:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump(self):
            return self.__dict__


async def serve_acp_async(
    agent: AnyAgent,
    serving_config: Optional[ACPServingConfig] = None,
) -> ServerHandle:
    """Serve an agent using the Agent Connect Protocol (ACP).

    This function starts an ACP-compliant server that exposes the agent's
    capabilities via REST API, following Linux Foundation Agentcy standards.

    Args:
        agent: The agent to serve
        serving_config: ACP serving configuration

    Returns:
        ServerHandle for managing the server

    Raises:
        ImportError: If ACP dependencies are not installed

    Example:
        >>> from any_agent import AnyAgent, AgentConfig
        >>> from any_agent.serving import ACPServingConfig, serve_acp_async
        >>>
        >>> agent = await AnyAgent.create_async("tinyagent", AgentConfig(...))
        >>> config = ACPServingConfig(port=8090, identity_id="did:agntcy:dev:org:agent")
        >>> server_handle = await serve_acp_async(agent, config)

    """
    if not acp_available and serving_config is None:
        msg = "You need to `pip install 'agntcy-acp'` to use ACP serving"
        raise ImportError(msg)
    
    # Use default config if not provided
    if serving_config is None:
        serving_config = ACPServingConfig()
    
    # Create ACP app
    app = await _get_acp_app_async(agent, serving_config)
    
    # Start server
    server_handle = await _start_uvicorn_server(app, serving_config)
    
    # Log startup information
    bridge_url = f"http://{serving_config.host}:{serving_config.port}{serving_config.endpoint}"
    
    if serving_config.identity_id:
        logger.info(
            f"ACP server started at {bridge_url} with identity {serving_config.identity_id}"
        )
    else:
        logger.info(f"ACP server started at {bridge_url}")
    
    logger.info(f"ACP manifest available at: {bridge_url}/agents")
    
    return server_handle


async def _get_acp_app_async(
    agent: AnyAgent,
    serving_config: ACPServingConfig,
) -> "Starlette":
    """Create the ACP Starlette application.

    Args:
        agent: The agent to serve
        serving_config: ACP serving configuration

    Returns:
        Configured Starlette application

    """
    try:
        from starlette.applications import Starlette
        from starlette.routing import Route
        from starlette.responses import JSONResponse
    except ImportError as e:
        msg = "You need to `pip install 'starlette uvicorn'` to run ACP server"
        raise ImportError(msg) from e
    
    # Create executor
    executor = ACPAgentExecutor(agent, serving_config)
    await executor.initialize()
    
    # Define route handlers
    async def get_agents(request):
        """List available agents."""
        agents = executor.get_agents()
        return JSONResponse([a.model_dump() if hasattr(a, 'model_dump') else a for a in agents])
    
    async def search_agents(request):
        """Search agents - returns matching agents."""
        # For simplicity, return all agents
        return await get_agents(request)
    
    async def get_agent_by_id(request):
        """Get specific agent by ID."""
        agent_id = request.path_params["agent_id"]
        agent = executor.get_agent_by_id(agent_id)
        
        if agent is None:
            return JSONResponse({"error": "Agent not found"}, status_code=404)
        
        return JSONResponse(agent.model_dump() if hasattr(agent, 'model_dump') else agent)
    
    async def create_stateless_run(request):
        """Create a stateless run."""
        try:
            body = await request.json()
            result = await executor.execute_stateless_run(body)
            
            result_dict = result.model_dump() if hasattr(result, 'model_dump') else result
            return JSONResponse(result_dict)
            
        except Exception as e:
            logger.error(f"Error in create_stateless_run: {e}")
            return JSONResponse({
                "id": "error",
                "status": "failed",
                "error": {"type": "RequestError", "message": str(e)},
                "output": {"error": str(e), "success": False}
            }, status_code=500)
    
    async def get_stateless_run(request):
        """Get stateless run status - not supported in stateless mode."""
        return JSONResponse(
            {"error": "Run history not supported in stateless mode"}, 
            status_code=501
        )
    
    # Create routes
    base_path = serving_config.endpoint.rstrip("/")
    routes = [
        Route(f"{base_path}/agents/search", search_agents, methods=["POST"]),
        Route(f"{base_path}/agents", get_agents, methods=["GET"]),
        Route(f"{base_path}/agents/{{agent_id}}", get_agent_by_id, methods=["GET"]),
        Route(f"{base_path}/runs/stateless", create_stateless_run, methods=["POST"]),
        Route(f"{base_path}/runs/stateless/{{run_id}}", get_stateless_run, methods=["GET"]),
    ]
    
    return Starlette(routes=routes)


async def _start_uvicorn_server(app, serving_config: ACPServingConfig) -> ServerHandle:
    """Start uvicorn server and return handle."""
    try:
        import uvicorn
    except ImportError as e:
        msg = "You need to `pip install 'uvicorn'` to run ACP server"
        raise ImportError(msg) from e
    
    # Create and start server
    config = uvicorn.Config(
        app,
        host=serving_config.host,
        port=serving_config.port,
        log_level=serving_config.log_level,
    )
    server = uvicorn.Server(config)
    
    # Start server in background
    task = asyncio.create_task(server.serve())
    
    # Wait for server to start
    while not server.started:
        await asyncio.sleep(0.1)
    
    return ServerHandle(task=task, server=server)