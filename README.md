# MCP-ACP Bridge Implementation

> **Personal Project**: Anivar Aravind  
> **Focus**: Protocol interoperability in Mozilla AI ecosystem

## Overview

This repository contains an implementation of a bridge between MCP (Model Context Protocol) and ACP (Agent Connect Protocol), building on work done across the Mozilla AI ecosystem.

## Background Work

This project builds on several contributions:

### Mozilla AI Contributions

**PR #154: AGNTCY Identity Support in mcpd**
- Repository: mozilla-ai/mcpd
- Added AGNTCY Identity support to mcpd
- Enables DID-based authentication for MCP servers

**PR #757: MCP-A2A Bridge in any-agent** 
- Repository: mozilla-ai/any-agent
- Implemented bridge from MCP to A2A protocol
- Allows MCP tools to work with A2A agents

**PR #113: Async Support in ACP SDK**
- Repository: agntcy/acp-sdk  
- Added async client capabilities to ACP SDK
- Improves performance for ACP integrations

## This Implementation

This project completes the protocol connectivity by adding an MCP-to-ACP bridge, allowing:
- MCP servers to be accessed via ACP REST API
- Integration with AGNTCY Identity system
- Async operation support

### Architecture

```
MCP Server → Bridge → ACP REST API
```

The bridge translates between:
- MCP tool calls ↔ ACP stateless runs
- MCP tool discovery ↔ ACP agent manifests
- Optional AGNTCY Identity integration

### Features

- Protocol translation between MCP and ACP
- Async implementation
- Optional identity support
- REST API endpoints following ACP specification

## Repository Structure

```
bridge/           # Core bridge implementation
examples/         # Usage examples  
tests/           # Test suite
docs/            # Documentation
```

## Quick Start

```bash
# Install dependencies
pip install any-agent
pip install agntcy-acp  # optional

# Run example
python examples/basic_demo.py
```

## Implementation Details

The bridge follows patterns established in the any-agent codebase:
- Modular configuration system
- Async-first architecture  
- Comprehensive error handling
- Optional dependency management

## Testing

```bash
pytest tests/
```

## Purpose

This work demonstrates practical protocol interoperability between different agent communication standards, building on existing Mozilla AI infrastructure and patterns.