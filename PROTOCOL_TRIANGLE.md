# Protocol Triangle & Mozilla AI Ecosystem

## The Protocol Triangle

```
                    MCP (Mozilla)
                   Model Context Protocol
                  /                    \
                 /                      \
                /                        \
               /                          \
      PR #757 /                            \ This Work
     (Merged)/                              \(POC)
            /                                \
           /                                  \
          v                                    v
    A2A (Google)  ←────────────────────→  ACP (Agentcy)
   Agent-to-Agent     Future: A2A-ACP      Agent Connect
    Protocol           Bridge (TBD)         Protocol
```

## Ecosystem Understanding

### Mozilla AI Components

**Core Infrastructure:**
- **any-agent**: Framework-agnostic agent library (async architecture)
- **mcpd**: MCP daemon for server management
- **agent-factory**: Natural language to agent code generator
- **lumigator**: LLM evaluation and benchmarking
- **any-llm**: LLM interaction framework

**Active Projects:**
- **document-to-podcast**: Content transformation agents
- **lm-evaluation-harness**: Model evaluation pipeline
- **wasm-agents-blueprint**: WebAssembly agent deployment

### Protocol Ecosystem

#### MCP (Model Context Protocol) - Mozilla
```
Purpose: Connect AI models to external tools and data
Architecture: Tool server ↔ MCP client ↔ AI model
Key Features:
- Tool discovery and execution
- Resource access (files, databases, APIs)
- Secure sandboxing
```

#### A2A (Agent-to-Agent Protocol) - Google
```
Purpose: Enable agent-to-agent communication
Architecture: Agent ↔ A2A protocol ↔ Agent
Key Features:
- Agent discovery and capability exchange
- Task delegation and coordination
- Stateful conversations
```

#### ACP (Agent Connect Protocol) - Agentcy
```
Purpose: REST-based agent services with enterprise features
Architecture: HTTP client ↔ ACP API ↔ Agent service
Key Features:
- REST API (stateless/stateful operations)
- W3C DID authentication
- Enterprise identity management
```

## Bridge Implementations

### PR #757: MCP → A2A Bridge (Merged)
**Location:** mozilla-ai/any-agent
**Function:** Expose MCP tools as A2A-compatible agents
**Pattern:** Protocol translation + async architecture

### This Work: MCP → ACP Bridge (POC)
**Location:** This repository
**Function:** Expose MCP tools as ACP REST services  
**Pattern:** Following established any-agent patterns

### Future: A2A → ACP Bridge (TBD)
**Function:** Direct A2A to ACP communication
**Benefit:** Complete triangle connectivity

## Identity Integration

### AGNTCY Identity (PR #154)
**Standard:** W3C DID + Verifiable Credentials
**Format:** `did:agntcy:dev:{org}:{server}`
**Integration:** mcpd identity support

### Enterprise Authentication Flow
```
1. Agent requests service access
2. Present DID credentials
3. Verify identity via AGNTCY resolver
4. Authorize tool/service access
5. Execute with verified identity
```

## Async Architecture Transformation

### Before (Sync)
- Blocking tool calls
- Single request/response
- Performance bottlenecks

### After (Async + This Work)
- Non-blocking operations
- Concurrent tool execution
- Production-scale performance

## Complete Ecosystem View

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MCP Servers   │    │   A2A Agents    │    │  ACP Services   │
│                 │    │                 │    │                 │
│ • Filesystem    │    │ • Orchestrators │    │ • Enterprise    │
│ • Database      │    │ • Coordinators  │    │ • REST APIs     │
│ • Web APIs      │    │ • Task Managers │    │ • Identity      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────┬───────────┼───────────┬───────────┘
                     │           │           │
              ┌─────────────────────────────────────────┐
              │        Mozilla AI Ecosystem            │
              │                                         │
              │ • any-agent (async framework)          │
              │ • mcpd (MCP daemon)                     │
              │ • agent-factory (code generation)      │
              │ • lumigator (evaluation)                │
              │ • Identity integration (W3C DIDs)      │
              └─────────────────────────────────────────┘
```

## Strategic Value

### Technical Integration
- **Complete interoperability** across all major agent protocols
- **Standards compliance** with W3C identity specifications
- **Production architecture** with async-first design

### Ecosystem Positioning
- **Mozilla leadership** in agent protocol standards
- **Enterprise adoption** through identity and REST APIs
- **Developer experience** with unified toolchain

### Future Roadmap
- Complete triangle implementation (A2A ↔ ACP)
- Advanced identity features
- Production deployment patterns