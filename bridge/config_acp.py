"""Configuration for MCP-ACP bridge serving."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from any_agent.config import MCPParams


class MCPToACPBridgeConfig(BaseModel):
    """Configuration for MCP to ACP bridge.
    
    Example:
        bridge_config = MCPToACPBridgeConfig(
            mcp_config=mcp_params,
            host="localhost",
            port=8090,
            endpoint="/mcp-bridge",
            server_name="filesystem-server",
            organization="mozilla-ai",
            identity_id="did:agntcy:dev:mozilla-ai:filesystem-server"
        )
    """

    model_config = ConfigDict(extra="forbid")

    mcp_config: MCPParams
    """MCP server configuration to bridge."""

    host: str = Field(default="localhost", description="Host to serve on")
    """Will be passed as argument to `uvicorn.run`."""

    port: int = Field(default=8090, description="Port to serve on")
    """Will be passed as argument to `uvicorn.run`."""

    endpoint: str = Field(default="/mcp-bridge", description="Endpoint path")
    """Will be pass as argument to `Starlette().add_route`"""

    log_level: str = Field(default="warning", description="Log level for uvicorn server")
    """Will be passed as argument to the `uvicorn` server."""

    server_name: str = Field(default="mcp-server", description="MCP server name")
    """Identifier for the MCP server being bridged."""

    identity_id: Optional[str] = Field(
        default=None, 
        description="AGNTCY Identity DID for the bridge"
    )
    """Optional AGNTCY Identity DID for enterprise authentication."""

    version: str = Field(default="1.0.0", description="Version of the bridge")
    """Version identifier for the bridge service."""

    organization: str = Field(default="any-agent", description="Organization name")
    """Organization name for metadata and identity."""