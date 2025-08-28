# MCP-ACP Bridge Demo

Working implementation of a bridge that lets MCP tools work with ACP's REST API.

📖 **[Read the Vision](VISION.md)** - Why identity-first protocol interoperability matters

## What This Is

A proof-of-concept showing:
- MCP tools accessible via REST endpoints
- Identity metadata in API responses  
- Working examples you can run

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run basic demo
python examples/basic_demo.py

# Run with identity simulation
python examples/mcpd_integration_demo.py

# Run mcpd REST API demo (agent-factory approach)
python examples/mcpd_rest_demo.py
```

## How It Works

```
MCP Tools → Bridge → ACP REST API
```

The bridge translates MCP tool calls to ACP endpoints:
- `GET /agents` - List available tools
- `POST /runs/stateless` - Execute a tool

## Example Usage

```python
from bridge.config_acp import MCPToACPBridgeConfig
from bridge.server_acp import serve_mcp_as_acp_async

# Configure bridge
config = MCPToACPBridgeConfig(
    mcp_command="uvx",
    mcp_args=["mcp-server-filesystem"],
    port=8090
)

# Start it
await serve_mcp_as_acp_async(config)
```

Now MCP tools are available at `http://localhost:8090`.

## With Identity

If you're using mcpd with identity:

```python
config = MCPToACPBridgeConfig(
    mcp_command="mcpd",
    mcp_args=["run", "my-server"],
    identity_id="did:agntcy:mcpd:org:server",
    port=8090
)
```

The identity appears in API responses for audit trails.

## Related Work

### Core Protocol Bridges
- [any-agent PR #757](https://github.com/mozilla-ai/any-agent/pull/757): MCP-to-A2A bridge
- [any-agent PR #774](https://github.com/mozilla-ai/any-agent/pull/774): MCP-to-ACP bridge  

### Identity & Infrastructure
- [mcpd PR #154](https://github.com/mozilla-ai/mcpd/pull/154): AGNTCY Identity support
- [agent-factory PR #310](https://github.com/mozilla-ai/agent-factory/pull/310): MCPStdio to mcpd migration

### Agent Improvements
- [any-agent PR #763](https://github.com/mozilla-ai/any-agent/pull/763): Reasoning tokens support
- [any-agent PR #762](https://github.com/mozilla-ai/any-agent/pull/762): Tool error schemas

📖 **[Full Contribution List](CONTRIBUTIONS.md)** - See all 22+ PRs across Mozilla AI and AGNTCY

## License

MIT
EOF < /dev/null