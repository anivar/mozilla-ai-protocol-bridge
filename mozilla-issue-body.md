## RFC: Add MCP-ACP Bridge for Linux Foundation Interoperability

### Background
Following my MCP-A2A bridge work in [PR #757](https://github.com/mozilla-ai/any-agent/pull/757), I'd like to propose adding an MCP-ACP bridge to complete protocol interoperability with the Linux Foundation's [Agentcy project](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agentcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos).

### Strategic Value
- **Complete Protocol Triangle**: MCP ↔ A2A ↔ ACP interoperability
- **Foundation Partnership**: Direct Mozilla ↔ Linux Foundation bridge
- **W3C Standards**: Integration with [DID Core](https://www.w3.org/TR/did-core/) and [Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)
- **Enterprise Adoption**: REST API access to MCP tools with enterprise authentication

### Technical Approach
This builds on established patterns from:
- **PR #757**: MCP-A2A bridge architecture and async patterns
- **[PR #154](https://github.com/mozilla-ai/mcpd/pull/154)**: W3C DID integration in Mozilla AI ecosystem
- **[PR #113](https://github.com/agntcy/acp-sdk/pull/113)**: Async ACP client capabilities

### Proof of Concept
I've implemented a working POC at: https://github.com/anivar/mozilla-ai-protocol-bridge

**Key features:**
- Protocol translation between MCP and ACP
- W3C DID authentication support
- Async architecture following any-agent patterns
- ACP-compliant REST API endpoints
- Working examples and documentation

### Proposed Integration
```
src/any_agent/serving/acp/
├── config_acp.py          # Configuration (similar to a2a)
├── bridge_executor.py     # Protocol translation logic
└── server_acp.py         # ACP server implementation
```

**Follows same patterns as:**
- `src/any_agent/serving/a2a/` (from PR #757)
- `src/any_agent/serving/mcp/` (existing)

### Use Cases
1. **Enterprise Integration**: Corporate MCP tools via ACP REST API
2. **Cross-Protocol Workflows**: A2A agents → ACP API → MCP tools
3. **Standards Compliance**: W3C DID authentication across protocols

### Implementation Plan
1. **Phase 1**: Integrate POC code following any-agent patterns
2. **Phase 2**: Add comprehensive tests matching existing standards
3. **Phase 3**: Documentation and examples
4. **Phase 4**: Optional dependency handling (like A2A integration)

Would this align with any-agent's interoperability mission? Happy to discuss implementation details or create a draft PR for review.

**Related Work:**
- MCP-A2A Bridge: [PR #757](https://github.com/mozilla-ai/any-agent/pull/757)
- W3C Identity in MCP: [mozilla-ai/mcpd#154](https://github.com/mozilla-ai/mcpd/pull/154)
- Async ACP Client: [agntcy/acp-sdk#113](https://github.com/agntcy/acp-sdk/pull/113)