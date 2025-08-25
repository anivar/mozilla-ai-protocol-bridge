## Add Mozilla MCP Integration Example

### Background
Following my async client work in [PR #113](https://github.com/agntcy/acp-sdk/pull/113), I'd like to contribute a Mozilla MCP integration example demonstrating practical ACP SDK usage with a major open source AI foundation.

### Strategic Value
- **Foundation Adoption**: Shows Mozilla AI ecosystem adopting ACP/Agentcy standards
- **Real-World Integration**: Practical example of cross-protocol communication
- **Linux Foundation Mission**: Concrete progress on "breaking down AI agent silos"
- **Async Client Showcase**: Demonstrates async capabilities from PR #113

### Integration Example
I've built a working MCP-ACP bridge that:
- Exposes Mozilla MCP tools via ACP REST API
- Uses async ACP client (from PR #113)
- Implements W3C DID authentication
- Follows [Agentcy identity specifications](https://spec.identity.agntcy.org/)

**Repository**: https://github.com/anivar/mozilla-ai-protocol-bridge

### Proposed Contribution
Add as ecosystem integration example:

```
examples/integrations/mozilla-mcp/
├── README.md                    # Integration guide
├── mcp_acp_bridge.py           # Bridge implementation
├── demo.py                     # Working example
├── requirements.txt            # Dependencies
└── docker-compose.yml          # Easy setup
```

### Technical Details
- **Protocol Translation**: MCP tools ↔ ACP REST endpoints
- **Authentication**: W3C DID integration per Agentcy specs
- **Architecture**: Async-first using ACP SDK patterns
- **Standards**: Compliant with both MCP and ACP specifications

### Use Cases Demonstrated
1. **Enterprise Integration**: Corporate MCP tools with ACP authentication
2. **Cross-Foundation**: Mozilla tools accessible via Linux Foundation protocol
3. **Standards Implementation**: W3C DID + Verifiable Credentials in practice

### Related Mozilla Work
This connects with broader Mozilla AI ecosystem integration:
- **[mozilla-ai/any-agent#757](https://github.com/mozilla-ai/any-agent/pull/757)**: MCP-A2A bridge
- **[mozilla-ai/mcpd#154](https://github.com/mozilla-ai/mcpd/pull/154)**: W3C DID support in MCP daemon

### Benefits to ACP SDK
- Shows real-world async client usage
- Demonstrates enterprise authentication patterns  
- Provides complete working example
- Showcases foundation-level adoption

Would this integration example be valuable for the ACP SDK ecosystem? Happy to adapt the contribution format to match project preferences.

The implementation is production-ready and could serve as both documentation and demonstration of ACP capabilities with major open source AI tools.