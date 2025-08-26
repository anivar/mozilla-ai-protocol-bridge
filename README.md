# MCP-ACP Bridge: Protocol Interoperability for AI Agent Ecosystem

> **Personal Project**: Anivar Aravind  
> **Mission**: Connecting Mozilla AI, Linux Foundation, Google, and W3C standards for agent protocol interoperability

## Project Overview

This project implements a bridge between Mozilla's Model Context Protocol (MCP) and Agentcy's Agent Connect Protocol (ACP), contributing to broader protocol interoperability in the AI agent ecosystem.

## Protocol Integration Approach

```
                    MCP (Mozilla)
                   Model Context Protocol
                    Tools & Resources
                        /              \
                       /                \
              PR #757 /                  \ PR #774
          (any-agent) /                    \ (POC)
                     /                      \
                    v                        v
        A2A (Google LF)                   ACP (AGNTCY LF)
       Agent-to-Agent                    Agent Connect Protocol
        Protocol                         + W3C Identity Standards
```

**Ecosystem Components:**
- **Mozilla AI**: MCP protocol for tool-to-model integration
- **Google**: A2A protocol for agent-to-agent communication  
- **Linux Foundation**: [Agentcy project](https://github.com/agntcy) for [multi-agent infrastructure](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos)
- **W3C**: [Decentralized Identifiers (DIDs)](https://www.w3.org/TR/did-core/) and [Verifiable Credentials](https://www.w3.org/TR/vc-data-model/) standards

## Technical Architecture

```
┌─────────────────┐   HTTP/REST    ┌─────────────────┐   MCP Protocol   ┌─────────────────┐
│   ACP Client    │ ──────────────→ │  MCP-ACP Bridge │ ─────────────────→ │   MCP Server    │
│                 │                │                 │                   │                 │
│ • REST API      │ ←────────────── │ • Protocol      │ ←─────────────── │ • Tools         │
│ • W3C DIDs      │   JSON         │   Translation   │   Tool Results   │ • Files         │
│ • Verifiable    │                │ • Identity      │                   │ • Databases     │
│   Credentials   │                │   Verification  │                   │ • APIs          │
└─────────────────┘                └─────────────────┘                   └─────────────────┘
        ↑                                    ↑
        │                                    │
    Standards:                         Standards:
    • Linux Foundation                 • Mozilla AI
    • Agentcy Specs                   • MCP Protocol
    • W3C Identity                    • Async Architecture
```

## Related Contributions

### [PR #154: AGNTCY Identity Support in mcpd](https://github.com/mozilla-ai/mcpd/pull/154)
- **Repository**: [mozilla-ai/mcpd](https://github.com/mozilla-ai/mcpd)
- **Standards**: [W3C DIDs](https://www.w3.org/TR/did-core/) + [Agentcy Identity Spec](https://spec.identity.agntcy.org/)
- **Purpose**: W3C DID integration in Mozilla AI ecosystem
- **Format**: `did:agntcy:dev:{org}:{server}` following W3C standards
- **Status**: Open

### [PR #757: MCP-A2A Protocol Bridge](https://github.com/mozilla-ai/any-agent/pull/757)
- **Repository**: [mozilla-ai/any-agent](https://github.com/mozilla-ai/any-agent)
- **Purpose**: Mozilla MCP to Google A2A protocol translation
- **Architecture**: Async-first design patterns
- **Status**: Open

### [PR #113: Async ACP SDK Support](https://github.com/agntcy/acp-sdk/pull/113)
- **Repository**: [agntcy/acp-sdk](https://github.com/agntcy/acp-sdk)
- **Foundation**: [Linux Foundation Agentcy Project](https://github.com/agntcy)
- **Standards**: [ACP Protocol](https://spec.identity.agntcy.org/) with W3C Identity
- **Purpose**: Async client capabilities for ACP SDK
- **Status**: Open

### [PR #774: MCP-ACP Bridge](https://github.com/mozilla-ai/any-agent/pull/774)
- **Purpose**: Mozilla MCP to Linux Foundation ACP bridge
- **Standards**: MCP + ACP + W3C DIDs + Verifiable Credentials
- **Implementation**: Production-ready with this POC as reference

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