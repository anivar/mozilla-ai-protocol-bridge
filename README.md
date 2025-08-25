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
              PR #757 /                  \ This Work
          (any-agent) /                    \ (POC)
                     /                      \
                    v                        v
        A2A (Google)  ←────────────────→  ACP (Linux Foundation)
       Agent-to-Agent      Future Work     Agent Connect Protocol
        Protocol           (A2A-ACP)       + W3C Identity Standards
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

### This Work: MCP-ACP Bridge
- **Purpose**: Mozilla MCP to Linux Foundation ACP bridge
- **Standards**: MCP + ACP + W3C DIDs + Verifiable Credentials
- **Implementation**: Proof-of-concept with working examples

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

| Protocol | Mozilla MCP | Google A2A | Linux Foundation ACP |
|----------|-------------|-------------|---------------------|
| **Mozilla MCP** | Native | PR #757 | This Work |
| **Google A2A** | PR #757 | Native | Future Work |
| **Linux Foundation ACP** | This Work | Future Work | Native |

## Current Limitations

- Proof-of-concept implementation
- Limited to stateless operations
- Mock MCP client for demonstration
- Requires further testing for production use

## Contributing

This is a personal project demonstrating protocol interoperability concepts. The implementation follows established patterns and maintains compatibility with existing standards.

---

**Repository**: Working proof-of-concept for MCP-ACP protocol bridging with W3C standards compliance.