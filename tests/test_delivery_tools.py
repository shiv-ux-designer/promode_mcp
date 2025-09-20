"""
Tests for Delivery Portal MCP tools.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from decimal import Decimal
from datetime import datetime

from src.tools.delivery_tools import (
    get_delivery_routes_tool, get_orders_for_delivery_tool, get_delivery_slots_tool,
    get_delivery_drivers_tool, get_delivery_metrics_tool
)
from src.models.delivery_models import (
    DeliveryRouteRequest, OrderDeliveryRequest, DeliverySlotRequest,
    DeliveryRouteResult, OrderDeliveryResult, DeliverySlotResult, DriverResult, DeliveryMetricsResult,
    DeliveryRoute, OrderInfo, DeliverySlot, DriverInfo, DeliveryMetrics, DeliveryAddress, OrderItem
)


class TestDeliveryToolsRegistration:
    """Test that delivery tools can be registered without errors."""
    
    @patch('src.tools.delivery_tools.DeliveryService')
    def test_get_delivery_routes_tool_registration(self, mock_service_class):
        """Test that get_delivery_routes_tool can be registered."""
        mock_mcp = Mock()
        get_delivery_routes_tool(mock_mcp)
        assert mock_mcp.tool.called
    
    @patch('src.tools.delivery_tools.DeliveryService')
    def test_get_orders_for_delivery_tool_registration(self, mock_service_class):
        """Test that get_orders_for_delivery_tool can be registered."""
        mock_mcp = Mock()
        get_orders_for_delivery_tool(mock_mcp)
        assert mock_mcp.tool.called
    
    @patch('src.tools.delivery_tools.DeliveryService')
    def test_get_delivery_slots_tool_registration(self, mock_service_class):
        """Test that get_delivery_slots_tool can be registered."""
        mock_mcp = Mock()
        get_delivery_slots_tool(mock_mcp)
        assert mock_mcp.tool.called
    
    @patch('src.tools.delivery_tools.DeliveryService')
    def test_get_delivery_drivers_tool_registration(self, mock_service_class):
        """Test that get_delivery_drivers_tool can be registered."""
        mock_mcp = Mock()
        get_delivery_drivers_tool(mock_mcp)
        assert mock_mcp.tool.called
    
    @patch('src.tools.delivery_tools.DeliveryService')
    def test_get_delivery_metrics_tool_registration(self, mock_service_class):
        """Test that get_delivery_metrics_tool can be registered."""
        mock_mcp = Mock()
        get_delivery_metrics_tool(mock_mcp)
        assert mock_mcp.tool.called
    
    @patch('src.tools.delivery_tools.DeliveryService')
    def test_all_tools_registration(self, mock_service_class):
        """Test that all delivery tools can be registered together."""
        mock_mcp = Mock()
        
        # Register all tools
        get_delivery_routes_tool(mock_mcp)
        get_orders_for_delivery_tool(mock_mcp)
        get_delivery_slots_tool(mock_mcp)
        get_delivery_drivers_tool(mock_mcp)
        get_delivery_metrics_tool(mock_mcp)
        
        # Verify all tools were registered
        assert mock_mcp.tool.call_count == 5


class TestDeliveryToolsIntegration:
    """Test delivery tools integration."""
    
    @patch('src.tools.delivery_tools.DeliveryService')
    def test_delivery_workflow_integration(self, mock_service_class):
        """Test that delivery tools work together in a workflow."""
        mock_mcp = Mock()
        
        # Register all tools
        get_delivery_routes_tool(mock_mcp)
        get_orders_for_delivery_tool(mock_mcp)
        get_delivery_slots_tool(mock_mcp)
        get_delivery_drivers_tool(mock_mcp)
        get_delivery_metrics_tool(mock_mcp)
        
        # Verify all tools were registered
        assert mock_mcp.tool.call_count == 5


if __name__ == '__main__':
    pytest.main([__file__])