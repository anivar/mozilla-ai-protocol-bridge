"""MCP to ACP bridge executor for translating between protocols."""

import asyncio
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import uuid4

from any_agent.logging import logger

if TYPE_CHECKING:
    from any_agent.tools.mcp.mcp_client import MCPClient
    
from .config_acp import MCPToACPBridgeConfig

# Check if ACP is available
acp_available = False
try:
    from agntcy_acp import (
        RunCreateStateless,
        RunStateless,
        RunStatus,
        StreamingMode,
        StreamingModes,
    )
    acp_available = True
except ImportError:
    pass


class MCPToACPBridgeExecutor:
    """Executor that translates ACP requests to MCP tool calls."""

    def __init__(self, mcp_client: "MCPClient", bridge_config: MCPToACPBridgeConfig):
        """Initialize the executor.

        Args:
            mcp_client: Connected MCP client
            bridge_config: Bridge configuration
        """
        self.mcp_client = mcp_client
        self.bridge_config = bridge_config
        self._mcp_tools: Dict[str, Any] = {}
        self._agent_manifest: Optional[Dict[str, Any]] = None

    async def initialize(self) -> None:
        """Initialize by loading MCP tools and creating ACP manifest."""
        raw_tools = await self.mcp_client.list_raw_tools()
        self._mcp_tools = {tool.name: tool for tool in raw_tools}
        logger.info(f"Loaded {len(self._mcp_tools)} MCP tools")
        
        # Create ACP manifest
        self._agent_manifest = await self._create_acp_manifest()
    
    async def _create_acp_manifest(self) -> Dict[str, Any]:
        """Create ACP manifest from MCP tools."""
        mcp_tools = await self.mcp_client.list_raw_tools()
        
        # Build tool descriptions for manifest
        tools_description = []
        for tool in mcp_tools:
            tools_description.append({
                "name": tool.name,
                "description": tool.description or f"MCP tool: {tool.name}",
                "inputSchema": getattr(tool, 'inputSchema', {})
            })
        
        manifest = {
            "id": f"mcp-bridge-{self.bridge_config.server_name}",
            "name": f"{self.bridge_config.server_name} MCP Bridge",
            "version": self.bridge_config.version,
            "description": f"MCP server '{self.bridge_config.server_name}' exposed via ACP",
            "metadata": {
                "organization": self.bridge_config.organization,
                "bridge_type": "mcp-to-acp",
                "identity_id": self.bridge_config.identity_id,
            },
            "acp": {
                "version": "0.2.3",
                "capabilities": {
                    "stateless": True,
                    "stateful": False,
                    "threads": False,
                    "callbacks": False,
                    "streaming": StreamingModes(
                        stateless=StreamingMode.value,
                        stateful=None
                    ) if acp_available else {"stateless": "value", "stateful": None},
                    "interrupts": False,
                },
                "input": {
                    "type": "object",
                    "properties": {
                        "tool": {"type": "string", "description": "Tool name to call"},
                        "args": {"type": "object", "description": "Tool arguments"}
                    },
                    "required": ["tool"]
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "result": {"description": "Tool execution result"},
                        "error": {"type": "string", "description": "Error message if failed"}
                    }
                },
                "tools": tools_description,
            }
        }
        
        return manifest

    async def execute_stateless_run(self, run_request) -> Any:
        """Execute a stateless ACP run by calling appropriate MCP tool.

        Args:
            run_request: ACP run request

        Returns:
            ACP run result
        """
        run_id = str(uuid4())
        
        try:
            # Extract tool and args from config
            config = getattr(run_request, 'config', {}) or {}
            tool_name = config.get("tool")
            args = config.get("args", {})
            
            if not tool_name:
                # If no tool specified, try to infer from input
                if len(self._mcp_tools) == 1:
                    tool_name = list(self._mcp_tools.keys())[0]
                    input_data = getattr(run_request, 'input', None)
                    args = {"input": input_data} if input_data else {}
                else:
                    raise ValueError(
                        f"Multiple tools available: {list(self._mcp_tools.keys())}. "
                        "Please specify which tool to use in config.tool"
                    )
            
            # Validate tool exists
            if tool_name not in self._mcp_tools:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            # Call MCP tool
            logger.info(f"Calling MCP tool '{tool_name}' with args: {args}")
            
            # Get the callable tool
            tools = await self.mcp_client.list_tools()
            tool_func = next((t for t in tools if t.__name__ == tool_name), None)
            
            if not tool_func:
                raise ValueError(f"Tool {tool_name} not found in callable tools")
            
            # Execute the tool
            if asyncio.iscoroutinefunction(tool_func):
                result = await tool_func(**args)
            else:
                result = tool_func(**args)
            
            # Create successful run result
            if acp_available:
                return RunStateless(
                    id=run_id,
                    status=RunStatus.completed,
                    output={
                        "result": result,
                        "tool": tool_name,
                        "success": True
                    }
                )
            else:
                # Fallback for when ACP not available
                return {
                    "id": run_id,
                    "status": "completed",
                    "output": {
                        "result": result,
                        "tool": tool_name,
                        "success": True
                    }
                }
            
        except Exception as e:
            logger.error(f"Error executing MCP tool: {e}")
            
            if acp_available:
                return RunStateless(
                    id=run_id,
                    status=RunStatus.failed,
                    error={
                        "type": "ToolExecutionError",
                        "message": str(e)
                    },
                    output={
                        "error": str(e),
                        "success": False
                    }
                )
            else:
                # Fallback for when ACP not available
                return {
                    "id": run_id,
                    "status": "failed",
                    "error": {
                        "type": "ToolExecutionError",
                        "message": str(e)
                    },
                    "output": {
                        "error": str(e),
                        "success": False
                    }
                }