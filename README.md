# Breaking Protocol Silos: MCP ↔ A2A ↔ ACP Interoperability

> **Developer**: Anivar Aravind  
> **Mission**: Enable any tool to work with any agent, regardless of protocol
> **Innovation**: First to implement identity-aware protocol bridging

## Why This Matters

The AI agent ecosystem is fragmented:
- **MCP** (Anthropic): Amazing tools, but isolated from agent protocols
- **A2A** (Google → Linux Foundation): Great for agents, limited tool access
- **ACP** (AGNTCY/Linux Foundation): Enterprise-ready, but new ecosystem

I'm solving this with protocol bridges that preserve cryptographic identity across all translations. This isn't just connecting protocols - it's building the foundation for enterprise-grade, verifiable AI agent interactions.

## Protocol Integration Approach

```
                    MCP (Anthropic)
                   Model Context Protocol
                    Tools & Resources
                        /              \
                       /                \
              PR #757 /                  \ PR #774
          (any-agent) /                    \ (this POC)
                     /                      \
                    v                        v
        A2A (Google LF)                   ACP (AGNTCY LF)
       Agent-to-Agent                    Agent Connect Protocol
        Protocol                         + W3C Identity Standards
```

**Key Players:**
- **Anthropic**: Created MCP for tool/model integration
- **Mozilla AI**: Hosts any-agent framework and mcpd daemon
- **Google**: Donated A2A protocol to Linux Foundation
- **AGNTCY**: Linux Foundation project for agent infrastructure
- **W3C**: Standards for identity (DIDs) and credentials

## Technical Architecture

```
┌─────────────────┐   HTTP/REST    ┌─────────────────┐   MCP Protocol   ┌─────────────────┐
│   ACP Client    │ ──────────────→ │  MCP-ACP Bridge │ ─────────────────→ │   MCP Server    │
│                 │                │                 │                   │                 │
│ • REST API      │ ←────────────── │ • Protocol      │ ←─────────────── │ • Tools         │
│ • W3C DIDs      │   JSON         │   Translation   │   Tool Results   │ • Resources     │
│ • Async SDK     │                │ • Identity      │                   │ • Databases     │
│   (PR #113)     │                │   Verification  │                   │ • APIs          │
└─────────────────┘                └─────────────────┘                   └─────────────────┘
        ↑                                    ↑
        │                                    │
    My Contributions:                  My Contributions:
    • PR #113 (AGNTCY)                • PR #154 (mcpd identity)
    • Async support                    • PR #774 (this bridge)
    • W3C Identity                    • PR #757 (A2A bridge)
```

## My Contributions Across Organizations

### Mozilla AI Repository Contributions

**[PR #154: AGNTCY Identity in mcpd](https://github.com/mozilla-ai/mcpd/pull/154)**
- Added cryptographic identity (Ed25519) to MCP servers
- W3C DID format: `did:agntcy:mcpd:{org}:{server}`
- Foundation for all protocol bridges

**[PR #757: MCP-to-A2A Bridge](https://github.com/mozilla-ai/any-agent/pull/757)**
- Bridges Anthropic's MCP to Google's A2A protocol
- Identity preserved for audit (A2A can't transmit it)
- Performance optimized with tool caching

**[PR #774: MCP-to-ACP Bridge](https://github.com/mozilla-ai/any-agent/pull/774)**
- Bridges MCP to AGNTCY's ACP protocol
- Full identity exposure via REST metadata
- Enterprise-ready with W3C standards

### Linux Foundation AGNTCY Contribution

**[PR #113: Async Support for ACP SDK](https://github.com/agntcy/acp-sdk/pull/113)**
- Critical async/await support for Python SDK
- Enables high-performance ACP integrations
- Required for the MCP-ACP bridge to work efficiently

This is significant: I'm contributing to both Mozilla AI and Linux Foundation projects to ensure they work together seamlessly.

## Why Not OAuth? The Identity Challenge

Traditional OAuth doesn't work for agent protocols:

1. **Non-Browser Environments**: MCP servers run as CLI tools, daemons, or background services - no browser for OAuth flow
2. **Machine-to-Machine**: Agents talk directly to each other without human intervention
3. **Protocol Constraints**: A2A doesn't support bearer tokens or headers; it's a custom wire protocol
4. **Startup Authentication**: Tools need identity verification at startup, not per-request
5. **Decentralized**: No central OAuth provider makes sense for distributed agent networks

That's why I'm using **AGNTCY Identity** with W3C DIDs:
- Works offline (no auth server needed)
- Cryptographic verification (Ed25519 signatures)
- Protocol agnostic (same identity across MCP, A2A, ACP)
- Machine-friendly (no human in the loop)

## W3C Standards Implementation

### Identity Architecture
```yaml
Identity Layer (W3C Standards):
  - DID Core Specification: https://www.w3.org/TR/did-core/
  - Verifiable Credentials: https://www.w3.org/TR/vc-data-model/
  - Agentcy Implementation: https://spec.identity.agntcy.org/

Protocol Layer:
  - Mozilla MCP: Tool-to-model communication
  - Google A2A: Agent-to-agent workflows  
  - Linux Foundation ACP: Enterprise agent services

Bridge Layer:
  - Cross-protocol translation
  - Standards-compliant identity verification
  - Async architecture
```

### Authentication Flow
1. **Identity Creation**: Generate W3C DID following Agentcy specifications
2. **Credential Issuance**: Create Verifiable Credentials for authorization
3. **Protocol Translation**: Bridge requests between MCP and ACP with identity verification
4. **Standards Compliance**: Maintain W3C and foundation specifications

## Identity Integration Across Protocol Bridges

All protocol bridges leverage AGNTCY Identity from mcpd for secure, verifiable tool execution:

### 1. Foundation: mcpd PR #154
- **Purpose**: Generates cryptographic identity for MCP servers
- **Format**: `did:agntcy:mcpd:{organization}:{server}`
- **Example**: `did:agntcy:mcpd:mozilla-ai:github-tools`

### 2. MCP-to-A2A Bridge (PR #757)
- **Uses**: Identity from mcpd for logging and audit trails
- **Limitation**: A2A protocol doesn't support metadata, so identity is logged but not transmitted to clients
- **Benefit**: Complete audit trail for enterprise compliance

### 3. MCP-to-ACP Bridge (PR #774)
- **Uses**: Identity from mcpd AND exposes it in ACP metadata
- **Advantage**: ACP clients can verify tool authenticity
- **Format**: Identity included in agent manifest and tool execution metadata

### 4. Complete Identity Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Mozilla AI Ecosystem with Identity                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐    generates     ┌─────────────────────────────┐      │
│  │   mcpd   │ ───────────────> │ did:agntcy:mcpd:org:server │      │
│  │  PR #154 │                  │    (W3C DID + Ed25519)      │      │
│  └──────────┘                  └──────────┬──────────────────┘      │
│                                           │                          │
│                                           │ uses                     │
│                                           ▼                          │
│                                  ┌─────────────────┐                 │
│                                  │   MCP Server    │                 │
│                                  │ (runs with DID) │                 │
│                                  └────────┬────────┘                 │
│                                          │                           │
│                    ┌─────────────────────┴─────────────────────┐     │
│                    │                                           │     │
│                    ▼                                           ▼     │
│  ┌─────────────────────────────┐              ┌─────────────────────┐│
│  │       any-agent             │              │      any-agent      ││
│  ├─────────────────────────────┤              ├─────────────────────┤│
│  │ • Framework for agents      │              │ • Same framework    ││
│  │ • Uses any-llm internally   │              │ • Uses any-llm      ││
│  │                             │              │                     ││
│  │ ┌───────────────────┐       │              │ ┌─────────────────┐ ││
│  │ │ MCP-A2A Bridge    │       │              │ │ MCP-ACP Bridge  │ ││
│  │ │    PR #757        │       │              │ │    PR #774      │ ││
│  │ ├───────────────────┤       │              │ ├─────────────────┤ ││
│  │ │ • Reads identity  │       │              │ │ • Reads identity│ ││
│  │ │ • Logs for audit  │       │              │ │ • Exposes in API│ ││
│  │ │ • Can't transmit  │       │              │ │ • Clients verify│ ││
│  │ └───────────────────┘       │              │ └─────────────────┘ ││
│  └──────────┬──────────────────┘              └──────────┬──────────┘│
│             │                                             │           │
│             ▼                                             ▼           │
│  ┌───────────────────┐                        ┌────────────────┐     │
│  │   A2A Protocol    │                        │  ACP Protocol  │     │
│  │ (Google/LF)       │                        │ (AGNTCY/LF)    │     │
│  │                   │                        │                │     │
│  │ No metadata field │                        │ Full metadata  │     │
│  │ for identity      │                        │ support         │     │
│  └───────────────────┘                        └────────────────┘     │
│             │                                             │           │
│             ▼                                             ▼           │
│  ┌─────────────────────────────────────────────────────────────┐     │
│  │                         any-llm                             │     │
│  │                    (Common LLM Layer)                       │     │
│  │  • Unified interface for multiple LLM providers            │     │
│  │  • Used by any-agent for model interactions                │     │
│  │  • Supports OpenAI, Anthropic, Google, etc.                │     │
│  └─────────────────────────────────────────────────────────────┘     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 5. Identity Flow Sequence

```
Step 1: Identity Generation
┌──────┐                      ┌──────────┐
│ User │                      │   mcpd   │
└──┬───┘                      └────┬─────┘
   │                               │
   │ mcpd identity init server     │
   │─────────────────────────────>│
   │                               │ generates Ed25519 keys
   │                               │ creates DID document
   │<─────────────────────────────│
   │ did:agntcy:mcpd:org:server   │
   │                               │

Step 2: MCP Server with Identity
┌──────────┐                  ┌─────────────┐
│   mcpd   │                  │ MCP Server  │
└────┬─────┘                  └──────┬──────┘
     │                               │
     │ mcpd run server              │
     │─────────────────────────────>│
     │ verifies identity            │
     │ starts server with DID       │
     │                               │

Step 3a: MCP-to-A2A Bridge (PR #757)
┌─────────────┐              ┌──────────────┐              ┌────────┐
│ MCP Server  │              │ any-agent    │              │  A2A   │
│  (with DID) │              │ MCP-A2A Bridge│              │ Client │
└──────┬──────┘              └───────┬──────┘              └───┬────┘
       │                             │                          │
       │<────── connect with DID ────│                          │
       │                             │                          │
       │────── tools available ─────>│                          │
       │                             │                          │
       │                             │<──── request tools ──────│
       │                             │                          │
       │                             │ logs: "using identity    │
       │                             │  did:agntcy:..."         │
       │                             │                          │
       │<────── execute tool ────────│                          │
       │                             │                          │
       │────── tool result ─────────>│────── result ──────────>│
       │                             │ (no identity in A2A)     │

Step 3b: MCP-to-ACP Bridge (PR #774)
┌─────────────┐              ┌──────────────┐              ┌────────┐
│ MCP Server  │              │ any-agent    │              │  ACP   │
│  (with DID) │              │ MCP-ACP Bridge│              │ Client │
└──────┬──────┘              └───────┬──────┘              └───┬────┘
       │                             │                          │
       │<────── connect with DID ────│                          │
       │                             │                          │
       │────── tools available ─────>│                          │
       │                             │                          │
       │                             │<──── GET /agents ────────│
       │                             │                          │
       │                             │────── manifest ─────────>│
       │                             │ {metadata: {             │
       │                             │   identity_id: "did:..." │
       │                             │ }}                       │
       │                             │                          │
       │<────── execute tool ────────│<──── POST /runs ────────│
       │                             │                          │
       │────── tool result ─────────>│────── result + DID ─────>│
```

This unified identity approach ensures:
- Single source of truth for identity (mcpd)
- Consistent identity across all protocols
- Enterprise-grade security and compliance
- W3C standards compliance throughout

## Implementation

### Basic Configuration
```python
from bridge.config_acp import MCPToACPBridgeConfig
from bridge.server_acp import serve_mcp_as_acp_async

# Configure bridge
bridge_config = MCPToACPBridgeConfig(
    mcp_command="npx",
    mcp_args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    host="localhost",
    port=8090,
    endpoint="/mcp-bridge",
    identity_id="did:agntcy:dev:demo-org:fs-server",
    organization="demo-org"
)

# Start bridge
server = await serve_mcp_as_acp_async(bridge_config)
```

### API Usage
```bash
# W3C Identity Authentication
export IDENTITY_DID="did:agntcy:dev:demo-org:fs-server"
export ORG_CREDENTIAL="demo-org"

# ACP API calls
curl -H "X-W3C-DID: $IDENTITY_DID" \
     -H "X-Agentcy-Org: $ORG_CREDENTIAL" \
     http://localhost:8090/mcp-bridge/agents

# Tool execution
curl -X POST http://localhost:8090/mcp-bridge/runs/stateless \
  -H "Content-Type: application/json" \
  -H "X-W3C-DID: $IDENTITY_DID" \
  -d '{"config": {"tool": "read_file", "args": {"path": "/tmp/data.txt"}}}'
```

## Use Cases

### Enterprise Integration
- Corporate MCP tools accessible via ACP REST API
- W3C DID authentication for secure access
- Standards-compliant identity verification

### Cross-Protocol Communication
- Bridge between different agent protocol ecosystems
- Enable tool sharing across protocol boundaries
- Maintain protocol-specific optimizations

### Standards Compliance
- W3C DID Core implementation
- Verifiable Credentials support
- Foundation-specific protocol adherence

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Basic demo
python examples/basic_demo.py

# Advanced demo with identity
python examples/advanced_demo.py

# Test API
curl http://localhost:8090/mcp-bridge/agents
```

## Project Structure

```
bridge/
├── config_acp.py          # Configuration management
├── bridge_executor.py     # Protocol translation logic
└── server_acp.py         # ACP server implementation

examples/
├── basic_demo.py          # Basic usage example
└── advanced_demo.py       # Enterprise features demo

tests/
└── test_bridge.py         # Test suite
```

## Standards and Specifications

- **[W3C Decentralized Identifiers](https://www.w3.org/TR/did-core/)**: Universal identity layer
- **[W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)**: Authentication framework
- **[Agentcy Specifications](https://spec.identity.agntcy.org/)**: Implementation guidelines
- **[Linux Foundation Announcement](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos)**: Industry standardization

## Protocol Interoperability Status

| Protocol | Mozilla MCP | Google A2A (LF) | AGNTCY ACP (LF) |
|----------|-------------|-----------------|------------------|
| **Mozilla MCP** | Native | PR #757 | PR #774 |
| **Google A2A (LF)** | PR #757 | Native | LF Working On |
| **AGNTCY ACP (LF)** | PR #774 | LF Working On | Native |

## Current Limitations

- Proof-of-concept implementation
- Limited to stateless operations
- Mock MCP client for demonstration
- Requires further testing for production use

## Contributing

This is a personal project demonstrating protocol interoperability concepts. The implementation follows established patterns and maintains compatibility with existing standards.

---

**Repository**: Working proof-of-concept for MCP-ACP protocol bridging with W3C standards compliance.