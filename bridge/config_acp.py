"""Configuration for MCP-ACP bridge serving."""

from typing import Optional, Dict, Any

from pydantic import BaseModel, ConfigDict, Field


class MCPConfig(BaseModel):
    """Simple MCP configuration for the bridge."""
    command: str
    args: list[str]
    env: Optional[Dict[str, str]] = None


class MCPToACPBridgeConfig(BaseModel):
    """Configuration for MCP to ACP bridge.
    
    Example:
        bridge_config = MCPToACPBridgeConfig(
            mcp_command="npx",
            mcp_args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
            host="localhost",
            port=8090,
            endpoint="/mcp-bridge",
            server_name="filesystem-server",
            organization="demo-org",
            identity_id="did:agntcy:dev:demo-org:filesystem-server"
        )
    """

    model_config = ConfigDict(extra="forbid")

    # MCP Configuration
    mcp_command: str = Field(description="Command to start MCP server")
    mcp_args: list[str] = Field(default_factory=list, description="Arguments for MCP command")
    mcp_env: Optional[Dict[str, str]] = Field(default=None, description="Environment variables")

    # Server Configuration
    host: str = Field(default="localhost", description="Host to serve on")
    port: int = Field(default=8090, description="Port to serve on")
    endpoint: str = Field(default="/mcp-bridge", description="Endpoint path")
    log_level: str = Field(default="warning", description="Log level for uvicorn server")

    # Bridge Configuration
    server_name: str = Field(default="mcp-server", description="MCP server name")
    identity_id: Optional[str] = Field(default=None, description="AGNTCY Identity DID")
    version: str = Field(default="1.0.0", description="Version of the bridge")
    organization: str = Field(default="demo-org", description="Organization name")