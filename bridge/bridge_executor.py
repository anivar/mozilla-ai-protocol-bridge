"""MCP to ACP bridge executor for translating between protocols."""

import asyncio
import json
import subprocess
from typing import Any, Dict, List, Optional
from uuid import uuid4

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
    # Fallback classes when ACP not available
    class RunStatus:
        completed = "completed"
        failed = "failed"
    
    class RunCreateStateless:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    class RunStateless:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)


class SimpleMCPClient:
    """Simple MCP client for the bridge."""
    
    def __init__(self, config: MCPToACPBridgeConfig):
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self.tools: Dict[str, Any] = {}
    
    async def connect(self):
        """Start the MCP server process."""
        env = self.config.mcp_env or {}
        self.process = subprocess.Popen(
            [self.config.mcp_command] + self.config.mcp_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env={**env}
        )
        
        # Mock tool discovery - in real implementation this would use MCP protocol
        self.tools = {
            "echo": {"name": "echo", "description": "Echo back the input", "schema": {}},
            "list_files": {"name": "list_files", "description": "List files in directory", "schema": {}},
            "read_file": {"name": "read_file", "description": "Read file contents", "schema": {}},
        }
        
        await asyncio.sleep(0.1)  # Give process time to start
    
    async def disconnect(self):
        """Stop the MCP server process."""
        if self.process:
            self.process.terminate()
            self.process.wait()
    
    async def list_raw_tools(self):
        """List available tools."""
        return [type('Tool', (), tool) for tool in self.tools.values()]
    
    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Call a tool (mock implementation)."""
        if tool_name == "echo":
            return args.get("message", "Hello from MCP-ACP bridge!")
        elif tool_name == "list_files":
            return {"files": ["file1.txt", "file2.txt", "README.md"]}
        elif tool_name == "read_file":
            return f"Contents of {args.get('path', 'unknown')}"
        else:
            raise ValueError(f"Unknown tool: {tool_name}")


class MCPToACPBridgeExecutor:
    """Executor that translates ACP requests to MCP tool calls."""

    def __init__(self, mcp_client: SimpleMCPClient, bridge_config: MCPToACPBridgeConfig):
        """Initialize the executor."""
        self.mcp_client = mcp_client
        self.bridge_config = bridge_config
        self._mcp_tools: Dict[str, Any] = {}
        self._agent_manifest: Optional[Dict[str, Any]] = None

    async def initialize(self) -> None:
        """Initialize by loading MCP tools and creating ACP manifest."""
        await self.mcp_client.connect()
        raw_tools = await self.mcp_client.list_raw_tools()
        self._mcp_tools = {tool.name: tool for tool in raw_tools}
        print(f"Loaded {len(self._mcp_tools)} MCP tools")
        
        # Create ACP manifest
        self._agent_manifest = await self._create_acp_manifest()
    
    async def _create_acp_manifest(self) -> Dict[str, Any]:
        """Create ACP manifest from MCP tools."""
        raw_tools = await self.mcp_client.list_raw_tools()
        
        # Build tool descriptions for manifest
        tools_description = []
        for tool in raw_tools:
            tools_description.append({
                "name": tool.name,
                "description": getattr(tool, 'description', f"MCP tool: {tool.name}"),
                "inputSchema": getattr(tool, 'schema', {})
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
                    "streaming": {"stateless": "value", "stateful": None},
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
        """Execute a stateless ACP run by calling appropriate MCP tool."""
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
                    args = {"message": input_data} if input_data else {}
                else:
                    raise ValueError(
                        f"Multiple tools available: {list(self._mcp_tools.keys())}. "
                        "Please specify which tool to use in config.tool"
                    )
            
            # Validate tool exists
            if tool_name not in self._mcp_tools:
                raise ValueError(f"Unknown tool: {tool_name}")
            
            # Call MCP tool
            print(f"Calling MCP tool '{tool_name}' with args: {args}")
            result = await self.mcp_client.call_tool(tool_name, args)
            
            # Create successful run result
            return RunStateless(
                id=run_id,
                status=RunStatus.completed,
                output={
                    "result": result,
                    "tool": tool_name,
                    "success": True
                }
            )
            
        except Exception as e:
            print(f"Error executing MCP tool: {e}")
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
    
    async def cleanup(self):
        """Clean up resources."""
        if self.mcp_client:
            await self.mcp_client.disconnect()