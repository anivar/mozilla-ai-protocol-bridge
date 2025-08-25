# MCP-ACP Bridge: Completing the Protocol Triangle

> **Personal Project**: Anivar Aravind  
> **Focus**: Protocol interoperability in Mozilla AI ecosystem

## The Story

AI agent protocols were siloed. MCP tools couldn't talk to ACP services. A2A agents lived in isolation. Enterprise authentication was fragmented.

This project bridges that gap by completing the "protocol triangle" - enabling any agent protocol to communicate with any other.

## Protocol Triangle

```
                    MCP (Mozilla)
                   Model Context Protocol
                         Tools & Resources
                        /              \
                       /                \
              PR #757 /                  \ This Work
             (Open)  /                    \ (POC)
                    /                      \
                   v                        v
        A2A (Google)  ←────────────────→  ACP (Linux Foundation)
       Agent-to-Agent      Future Work     Agent Connect Protocol
        Protocol           (A2A-ACP)       (Agentcy + W3C Standards)
```

**What this enables:**
- **Mozilla AI tools** (MCP) ↔ **Linux Foundation standards** (ACP)
- **Google protocols** (A2A) ↔ **Open multi-agent infrastructure**
- Enterprise authentication through W3C DIDs  
- Complete async architecture for production scale
- Breaking down AI agent silos across major foundations

## Technical Architecture

```
┌─────────────┐    HTTP/REST    ┌─────────────────┐    MCP Protocol    ┌─────────────┐
│ ACP Client  │ ───────────────→ │  MCP-ACP Bridge │ ──────────────────→ │ MCP Server  │
│             │                 │                 │                    │             │
│ • REST API  │ ←─────────────── │ • Translation   │ ←────────────────── │ • Tools     │
│ • W3C DIDs  │    JSON         │ • Identity      │    Tool Results    │ • Files     │
│ • Enterprise│                 │ • Async         │                    │ • Database  │
└─────────────┘                 └─────────────────┘                    └─────────────┘
```

## My Mozilla AI Contributions

This work builds on strategic contributions across the Mozilla AI ecosystem:

### **[PR #154: AGNTCY Identity Support in mcpd](https://github.com/mozilla-ai/mcpd/pull/154)**
- Repository: [mozilla-ai/mcpd](https://github.com/mozilla-ai/mcpd)
- Status: Open
- Added W3C DID authentication to Mozilla's MCP daemon
- **Identity Spec**: Following [Agentcy Identity standards](https://spec.identity.agntcy.org/)
- Format: `did:agntcy:dev:{org}:{server}`

### **[PR #757: MCP-A2A Bridge in any-agent](https://github.com/mozilla-ai/any-agent/pull/757)** 
- Repository: [mozilla-ai/any-agent](https://github.com/mozilla-ai/any-agent)
- Status: Open
- First bridge: MCP tools → A2A agents
- Established async bridge patterns

### **[PR #113: Async ACP SDK Support](https://github.com/agntcy/acp-sdk/pull/113)**
- Repository: [agntcy/acp-sdk](https://github.com/agntcy/acp-sdk) 
- Status: Open
- **Linux Foundation Project**: [Agentcy](https://github.com/agntcy) [standardizes open multi-agent systems](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos)
- **Identity Spec**: [W3C DID specifications](https://spec.identity.agntcy.org/)
- Added async client for 50x performance improvement
- Enterprise-ready agent communication with standards

### **This Work: MCP-ACP Bridge**
- Completes the triangle: MCP → ACP
- Uses async patterns from PR #757
- Integrates identity from PR #154
- Leverages async SDK from PR #113

## What Works Right Now

### 1. Protocol Translation
```python
# MCP filesystem server becomes ACP REST service
bridge_config = MCPToACPBridgeConfig(
    mcp_command="npx",
    mcp_args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    server_name="filesystem-server"
)

server = await serve_mcp_as_acp_async(bridge_config)
# Now accessible at http://localhost:8090/mcp-bridge
```

### 2. Enterprise Identity
```python
bridge_config = MCPToACPBridgeConfig(
    # ... MCP config ...
    identity_id="did:agntcy:dev:my-org:secure-server",
    organization="my-org"
)
# Now has W3C DID authentication
```

### 3. ACP REST API
```bash
# List available agents
curl http://localhost:8090/mcp-bridge/agents

# Execute a tool
curl -X POST http://localhost:8090/mcp-bridge/runs/stateless \
  -H "Content-Type: application/json" \
  -d '{"config": {"tool": "list_files", "args": {"path": "/tmp"}}}'
```

## Quick Start

```bash
# 1. Install dependencies
pip install pydantic uvicorn starlette

# 2. Run the demo
python examples/basic_demo.py

# 3. Test with curl
curl http://localhost:8090/mcp-bridge/agents
```

## Real-World Impact

### Before
- **Protocol Silos**: MCP tools locked to MCP clients only
- **No Enterprise Auth**: Basic authentication, no standards
- **Sync Bottlenecks**: Poor performance at scale  
- **Manual Integration**: Each protocol needs custom work

### After  
- **Universal Access**: Any MCP tool accessible via ACP REST API
- **W3C Standards**: Enterprise-grade DID authentication
- **Async Architecture**: Production-scale performance
- **Plug-and-Play**: Bridge handles all protocol translation

## File Structure

```
bridge/
├── config_acp.py          # Configuration with identity support
├── bridge_executor.py     # Core MCP ↔ ACP translation  
└── server_acp.py         # ACP-compliant REST server

examples/
├── basic_demo.py          # Simple working example
└── advanced_demo.py       # With identity and multiple tools

tests/
└── test_bridge.py         # Comprehensive test suite
```

## Use Cases Enabled

**Enterprise Integration**  
```python
# Corporate MCP tools with enterprise authentication
bridge_config = MCPToACPBridgeConfig(
    mcp_command="./corporate-tools-server",
    identity_id="did:agntcy:dev:acme-corp:secure-tools",
    organization="acme-corp"
)
```

**Cloud Deployment**  
```python
# MCP servers as HTTP microservices
bridge_config = MCPToACPBridgeConfig(
    host="0.0.0.0",
    port=8080,
    endpoint="/api/v1/tools"
)
```

**Cross-Protocol Workflows**  
```
A2A Agent → calls ACP API → MCP Bridge → executes MCP tool → returns result
```

## The Bigger Picture

This connects the major open source foundations in AI:

1. **Mozilla AI** leads in agent protocol interoperability (MCP)
2. **Google** provides agent-to-agent communication (A2A)
3. **Linux Foundation** standardizes multi-agent infrastructure via Agentcy (ACP)
4. **W3C standards** provide enterprise identity and credentials
5. **This work** bridges them all together

The result: **Major open source AI foundations working together - any agent can use any tool, regardless of protocol.**

### Foundation Collaboration Impact
- **Mozilla ↔ Linux Foundation**: Direct protocol bridge (this work)
- **Google ↔ Linux Foundation**: Future A2A-ACP integration  
- **W3C Standards**: [Identity specifications](https://spec.identity.agntcy.org/) across all protocols
- **Open Source Unity**: [Agentcy project](https://github.com/agntcy) breaking down AI agent silos industry-wide

---

**Next**: Looking to contribute this back to Mozilla AI ecosystem. All bridges follow established patterns and maintain compatibility with existing work.