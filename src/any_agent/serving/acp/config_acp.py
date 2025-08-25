"""Configuration for MCP-ACP bridge serving.

Following patterns from any_agent.serving.a2a.config_a2a and any_agent.serving.mcp.config_mcp
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ACPServingConfig(BaseModel):
    """Configuration for serving an agent using the Agent Connect Protocol (ACP).

    This enables MCP servers to be exposed as ACP services, following the
    Linux Foundation Agentcy project standards.

    Example:
        config = ACPServingConfig(
            port=8090,
            endpoint="/acp-bridge",
            identity_id="did:agntcy:dev:org:server"
        )

    """

    model_config = ConfigDict(extra="forbid")

    host: str = "localhost"
    """Will be passed as argument to `uvicorn.run`."""

    port: int = 8090
    """Will be passed as argument to `uvicorn.run`."""

    endpoint: str = "/acp"
    """Will be passed as argument to `Starlette().add_route`"""

    log_level: str = "warning"
    """Will be passed as argument to the `uvicorn` server."""

    version: str = "1.0.0"
    """Version of the ACP bridge service."""

    # ACP-specific configuration
    server_name: str = Field(default="any-agent", description="Server identifier")
    """Name identifier for the server being bridged."""

    organization: str = Field(default="any-agent", description="Organization name")
    """Organization name for metadata and identity."""

    identity_id: Optional[str] = Field(
        default=None,
        description="AGNTCY Identity DID (W3C format)"
    )
    """Optional AGNTCY Identity DID for enterprise authentication.
    
    Format: did:agntcy:dev:{org}:{server}
    See: https://spec.identity.agntcy.org/
    """

    # Streaming configuration (matching A2A patterns)
    stream_agent_responses: bool = True
    """Whether to stream agent responses via ACP."""

    stream_tool_usage: bool = False
    """Whether to stream tool execution results."""