# Breaking Protocol Silos: MCP ↔ A2A ↔ ACP Interoperability

> **Developer**: Anivar Aravind  
> **Mission**: Enterprise-grade AI agent infrastructure with cryptographic identity
> **Innovation**: First to implement verifiable cross-protocol agent interactions
> **Hub**: Mozilla AI - where all protocols converge for enterprise deployment

## Why This Matters

The AI agent ecosystem is fragmented:
- **MCP** (Anthropic): Amazing tools, but isolated from agent protocols
- **A2A** (Google → Linux Foundation): Great for agents, limited tool access
- **ACP** (AGNTCY/Linux Foundation): Enterprise-ready, but new ecosystem

I'm solving this by building enterprise AI infrastructure that corporations can trust:
- **Cryptographic identity** for every agent and tool interaction
- **Audit trails** built into the protocol layer
- **Compliance-ready** with W3C standards
- **Zero-trust architecture** where every call is verifiable

## Protocol Integration Approach

```
                    MCP (Anthropic)
                   Model Context Protocol
                    Tools & Resources
                            |
                            v
                    ┌─────────────────┐
                    │   Mozilla AI    │
                    │                 │
                    │  • any-agent    │
                    │  • mcpd         │
                    │  • Identity     │
                    └────┬───────┬────┘
                         /         \
                        /           \
               PR #757 /             \ PR #774
                      /               \
                     v                 v
        A2A (Google LF)              ACP (AGNTCY LF)
       Agent-to-Agent              Agent Connect Protocol
        Protocol                   + W3C Identity Standards
```

**Key Players:**
- **Mozilla AI**: The hub - hosts any-agent (multi-protocol framework) and mcpd (MCP daemon)
- **Anthropic**: Created MCP protocol for tool/model integration
- **Google**: Created A2A protocol, donated to Linux Foundation
- **AGNTCY**: Linux Foundation project with ACP protocol
- **W3C**: Standards for decentralized identity (DIDs)

## Technical Architecture

```
┌─────────────────┐                ┌─────────────────────┐                ┌─────────────────┐
│ AGNTCY/LF       │                │    Mozilla AI       │                │   Anthropic    │
│ ACP Client      │   HTTP/REST    │                     │  MCP Protocol  │   MCP Server   │
├─────────────────┤ ─────────────→ │  ┌───────────────┐  │ ─────────────→ ├─────────────────┤
│ • REST API      │                │  │ MCP-ACP Bridge│  │                │ • Tools         │
│ • W3C DIDs      │ ←───────────── │  │   (PR #774)   │  │ ←───────────── │ • Resources     │
│ • Async SDK     │   JSON + DID   │  │               │  │  Tool Results  │ • Databases     │
│   (PR #113)     │                │  │  any-agent    │  │                │ • APIs          │
└─────────────────┘                │  └───────────────┘  │                └─────────────────┘
                                   │                     │                          ↑
                                   │    mcpd identity    │                          │
                                   │      (PR #154)      │                     Runs via mcpd
                                   └─────────────────────┘                     (Mozilla AI)
```

## My Contributions Across Organizations

### Mozilla AI Ecosystem Contributions

**Protocol Interoperability (Focus of this POC):**
- **[PR #154](https://github.com/mozilla-ai/mcpd/pull/154)**: AGNTCY Identity in mcpd - cryptographic identity foundation
- **[PR #757](https://github.com/mozilla-ai/any-agent/pull/757)**: MCP-to-A2A bridge - protocol interoperability
- **[PR #774](https://github.com/mozilla-ai/any-agent/pull/774)**: MCP-to-ACP bridge - full identity exposure

**any-agent Framework Improvements:**
- **[PR #758](https://github.com/mozilla-ai/any-agent/pull/758)**: Fix A2A streaming callback accumulation
- **[PR #759](https://github.com/mozilla-ai/any-agent/pull/759)**: Improve MCP client lazy initialization
- **[PR #760](https://github.com/mozilla-ai/any-agent/pull/760)**: Add runtime context parameter for callbacks
- **[PR #762](https://github.com/mozilla-ai/any-agent/pull/762)**: Implement structured error schema for tools
- **[PR #763](https://github.com/mozilla-ai/any-agent/pull/763)**: Add reasoning/thinking tokens support

**any-llm Async Infrastructure:**
- **[PR #272](https://github.com/mozilla-ai/any-llm/pull/272)**: Response conversion utilities (merged)
- **[PR #254](https://github.com/mozilla-ai/any-llm/pull/254)**: OpenAI custom httpx client support
- **[PR #255](https://github.com/mozilla-ai/any-llm/pull/255)**: Native SDK providers httpx support

### Linux Foundation AGNTCY Contribution

**[PR #113: Async Support for ACP SDK](https://github.com/agntcy/acp-sdk/pull/113)**
- Critical async/await support for Python SDK
- Enables high-performance ACP integrations
- Required for the MCP-ACP bridge to work efficiently

I'm building enterprise-grade AI infrastructure with verifiable identity, async performance, and cross-protocol interoperability.

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

### The Mozilla AI Central Role

Mozilla AI is uniquely positioned as the convergence point:
- **any-agent**: The only framework supporting both A2A and future multi-protocol serving
- **mcpd**: The MCP daemon that Mozilla maintains, where I added identity support
- **Community**: Where protocol implementers collaborate on interoperability

My work leverages Mozilla AI's central position to bridge all protocols.

### 5. Identity Flow Sequence

```
Step 1: Identity Generation (in Mozilla's mcpd)
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

## Enterprise AI Use Cases

### Financial Services
- **Audit Requirements**: Every AI decision tracked with cryptographic proof
- **Compliance**: W3C DIDs provide regulatory-compliant identity trail
- **Risk Management**: Verify which AI agent made each trading decision

### Healthcare Systems  
- **HIPAA Compliance**: Identity verification for every data access
- **Chain of Custody**: Track which AI touched patient data
- **Multi-Organization**: Hospitals sharing AI tools with verified identity

### Manufacturing & Supply Chain
- **Zero Trust**: Every robot/AI interaction is cryptographically verified
- **Vendor Integration**: Connect AI systems across companies securely
- **Incident Response**: Complete audit trail when something goes wrong

### Why Enterprises Need This
- **Not just "AI"**: Enterprise AI with accountability
- **Not just "secure"**: Cryptographically verifiable
- **Not just "connected"**: Identity-aware interoperability

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