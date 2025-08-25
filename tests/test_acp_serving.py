"""Tests for ACP serving in any-agent.

Following patterns from any-agent's test suite.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.any_agent.serving.acp import ACPServingConfig, serve_acp_async


class TestACPServingConfig:
    """Test ACP serving configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = ACPServingConfig()
        
        assert config.host == "localhost"
        assert config.port == 8090
        assert config.endpoint == "/acp"
        assert config.server_name == "any-agent"
        assert config.identity_id is None
        assert config.version == "1.0.0"
        assert config.organization == "any-agent"
        assert config.stream_agent_responses is True
        assert config.stream_tool_usage is False
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = ACPServingConfig(
            host="0.0.0.0",
            port=9000,
            endpoint="/custom-acp",
            server_name="my-agent",
            identity_id="did:agntcy:dev:org:agent",
            version="2.0.0",
            organization="my-org"
        )
        
        assert config.host == "0.0.0.0"
        assert config.port == 9000
        assert config.endpoint == "/custom-acp"
        assert config.server_name == "my-agent"
        assert config.identity_id == "did:agntcy:dev:org:agent"
        assert config.version == "2.0.0"
        assert config.organization == "my-org"


@pytest.mark.asyncio
async def test_serve_acp_async_import_error():
    """Test proper error when dependencies missing."""
    # Mock missing imports
    import sys
    original_modules = {}
    
    # Remove ACP modules
    acp_modules = ["agntcy_acp", "starlette", "uvicorn"]
    for module in acp_modules:
        if module in sys.modules:
            original_modules[module] = sys.modules[module]
            del sys.modules[module]
    
    try:
        # Mock agent
        mock_agent = MagicMock()
        mock_agent.agent_config = MagicMock(description="Test agent")
        mock_agent.agent_framework = "tinyagent"
        mock_agent.get_tools = MagicMock(return_value=[])
        
        # Should raise ImportError
        with pytest.raises(ImportError) as exc_info:
            await serve_acp_async(mock_agent)
        
        assert "agntcy-acp" in str(exc_info.value) or "starlette" in str(exc_info.value)
        
    finally:
        # Restore modules
        for module, orig in original_modules.items():
            sys.modules[module] = orig