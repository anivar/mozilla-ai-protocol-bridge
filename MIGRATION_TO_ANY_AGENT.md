# Migration to any-agent Patterns

This POC has been migrated to follow proper any-agent patterns and architecture.

## Key Changes

### 1. Directory Structure
Now follows any-agent serving module patterns:
```
src/any_agent/serving/acp/
├── __init__.py          # Public API exports
├── config_acp.py        # ACPServingConfig (like A2AServingConfig)
├── server_acp.py        # serve_acp_async function
└── agent_executor.py    # ACPAgentExecutor class
```

### 2. Configuration Pattern
Following `A2AServingConfig` and `MCPServingConfig`:
```python
class ACPServingConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    host: str = "localhost"
    port: int = 8090
    endpoint: str = "/acp"
    # ACP-specific fields...
```

### 3. Server Pattern
Following `serve_a2a_async` and `serve_mcp_async`:
```python
async def serve_acp_async(
    agent: AnyAgent,
    serving_config: Optional[ACPServingConfig] = None,
) -> ServerHandle:
    """Serve an agent using Agent Connect Protocol."""
```

### 4. Integration with any-llm
The implementation is ready for any-llm patterns:
- Uses `AnyAgent` framework abstraction
- Compatible with all any-agent frameworks (tinyagent, langchain, etc.)
- Follows async patterns throughout

## Usage Example

```python
from any_agent import AgentConfig, AnyAgent
from any_agent.serving.acp import ACPServingConfig, serve_acp_async

# Create agent with any framework
agent = await AnyAgent.create_async(
    "tinyagent",  # or "langchain", "openai", etc.
    AgentConfig(
        model_id="anthropic/claude-3-haiku-20240307",  # any-llm pattern
        name="my-agent",
        tools=[...],
    )
)

# Serve via ACP
config = ACPServingConfig(
    port=8090,
    identity_id="did:agntcy:dev:org:agent"  # W3C DID
)
server = await serve_acp_async(agent, config)
```

## Benefits

1. **Framework Agnostic**: Works with any any-agent framework
2. **Standards Compliant**: Follows established any-agent patterns
3. **any-llm Ready**: Compatible with ongoing migration
4. **Production Patterns**: Uses same architecture as A2A and MCP serving

## Next Steps

1. Add to any-agent as `src/any_agent/serving/acp/`
2. Update main `__init__.py` to export ACP components
3. Add comprehensive tests following any-agent patterns
4. Documentation in standard any-agent format

This migration ensures the ACP bridge integrates seamlessly with any-agent's architecture and ongoing any-llm standardization.