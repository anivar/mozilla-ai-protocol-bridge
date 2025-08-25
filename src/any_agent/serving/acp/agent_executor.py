"""ACP agent executor for any-agent.

Following patterns from any_agent.serving.a2a.agent_executor
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import uuid4

from any_agent.logging import logger

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
        StreamingMode,
        StreamingModes,
    )
    acp_available = True
except ImportError:
    # Fallback classes when ACP not available
    class RunStatus:
        completed = "completed"
        failed = "failed"
    
    class RunStateless:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    class Agent:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump(self):
            return self.__dict__
    
    class AgentMetadata:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)


class ACPAgentExecutor:
    """Executor that bridges any-agent to ACP protocol."""

    def __init__(self, agent: AnyAgent, serving_config: ACPServingConfig):
        """Initialize the executor.

        Args:
            agent: The any-agent instance to serve
            serving_config: ACP serving configuration

        """
        self.agent = agent
        self.serving_config = serving_config
        self._agent_manifest: Optional[Dict[str, Any]] = None
        self._agent_id = f"any-agent-{serving_config.server_name}"

    async def initialize(self) -> None:
        """Initialize by creating ACP manifest from agent configuration."""
        # Get agent tools
        tools = self.agent.get_tools()
        
        # Create ACP manifest
        self._agent_manifest = await self._create_acp_manifest(tools)
        
        logger.info(f"ACP executor initialized with {len(tools)} tools")
    
    async def _create_acp_manifest(self, tools: List[Any]) -> Dict[str, Any]:
        """Create ACP manifest from agent tools."""
        # Build tool descriptions for manifest
        tools_description = []
        for tool in tools:
            tool_desc = {
                "name": getattr(tool, '__name__', str(tool)),
                "description": getattr(tool, '__doc__', '') or f"Tool: {tool}",
                "inputSchema": {}  # Could extract from tool signature
            }
            tools_description.append(tool_desc)
        
        manifest = {
            "id": self._agent_id,
            "name": f"{self.serving_config.server_name} (any-agent)",
            "version": self.serving_config.version,
            "description": self.agent.agent_config.description or "Any-agent served via ACP",
            "metadata": {
                "organization": self.serving_config.organization,
                "framework": str(self.agent.agent_framework),
                "model": self.agent.agent_config.model_id,
                "identity_id": self.serving_config.identity_id,
            },
            "acp": {
                "version": "0.2.3",
                "capabilities": {
                    "stateless": True,
                    "stateful": False,  # any-agent doesn't have built-in state
                    "threads": False,
                    "callbacks": False,
                    "streaming": {
                        "stateless": "value" if self.serving_config.stream_agent_responses else None,
                        "stateful": None
                    },
                    "interrupts": False,
                },
                "input": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "User query"},
                        "context": {"type": "object", "description": "Optional context"}
                    },
                    "required": ["query"]
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "result": {"description": "Agent response"},
                        "error": {"type": "string", "description": "Error message if failed"}
                    }
                },
                "tools": tools_description,
            }
        }
        
        return manifest

    def get_agents(self) -> List[Agent]:
        """Get list of available agents."""
        agent = Agent(
            id=self._agent_id,
            name=f"{self.serving_config.server_name} (any-agent)",
            description=self.agent.agent_config.description or "Any-agent served via ACP",
            metadata=AgentMetadata(
                organization=self.serving_config.organization,
                version=self.serving_config.version,
                framework=str(self.agent.agent_framework),
            ),
            acp_descriptor=self._agent_manifest.get("acp", {}),
        )
        return [agent]
    
    def get_agent_by_id(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        if agent_id == self._agent_id:
            return self.get_agents()[0]
        return None

    async def execute_stateless_run(self, run_request_data: Dict[str, Any]) -> RunStateless:
        """Execute a stateless ACP run using the any-agent.

        Args:
            run_request_data: Dictionary with run request data

        Returns:
            ACP run result

        """
        run_id = str(uuid4())
        
        try:
            # Extract query from request
            query = run_request_data.get("input", {}).get("query")
            if not query and isinstance(run_request_data.get("input"), str):
                query = run_request_data["input"]
            
            if not query:
                raise ValueError("No query provided in request")
            
            # Run the agent
            logger.info(f"Executing agent with query: {query}")
            
            # Use any-agent's run method
            if asyncio.iscoroutinefunction(self.agent.run):
                result = await self.agent.run(query)
            else:
                result = self.agent.run(query)
            
            # Format response
            if hasattr(result, 'final_output'):
                output_text = result.final_output
            else:
                output_text = str(result)
            
            # Create successful run result
            return RunStateless(
                id=run_id,
                status=RunStatus.completed,
                output={
                    "result": output_text,
                    "query": query,
                    "success": True
                }
            )
            
        except Exception as e:
            logger.error(f"Error executing agent: {e}")
            return RunStateless(
                id=run_id,
                status=RunStatus.failed,
                error={
                    "type": "AgentExecutionError",
                    "message": str(e)
                },
                output={
                    "error": str(e),
                    "success": False
                }
            )