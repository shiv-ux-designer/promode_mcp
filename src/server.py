# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""E-commerce MCP Server - AI-Enabled E-commerce Operations.

This is a Model Context Protocol (MCP) server that enables AI assistants to interact
with e-commerce systems and perform product catalog operations.

The server provides comprehensive tools for:
- Product browsing and search with filtering capabilities
- Category-based product organization
- Stock availability checking
- Price range filtering
- Product variant management

All functionality is organized into modular services for maintainability and extensibility.
"""

import asyncio
import logging
import os

from loguru import logger
from mcp.server.fastmcp import FastMCP

from .consts import ECOMMERCE_MCP_SERVER_APPLICATION_NAME
from .tools.ecommerce_tools import (
    browse_products_tool, get_category_counts_tool
)
from .tools.delivery_tools import (
    get_delivery_routes_tool, get_orders_for_delivery_tool, get_delivery_slots_tool,
    get_delivery_drivers_tool, get_delivery_metrics_tool
)
from .tools.super_admin_tools import (
    get_user_management_tool, get_system_health_tool, get_business_analytics_tool,
    get_security_audit_tool, get_system_config_tool
)
from .tools.supplier_tools import (
    get_supplier_management_tool, get_purchase_orders_tool, get_invoice_management_tool,
    get_supplier_analytics_tool, get_product_catalog_tool
)
from .tools.warehouse_tools import (
    get_inventory_management_tool, get_stock_movements_tool, get_warehouse_operations_tool,
    get_inventory_analytics_tool, get_quality_control_tool
)


def create_server() -> FastMCP:
    """Create and configure the E-commerce MCP server."""
    
    # Initialize the FastMCP server
    mcp = FastMCP(ECOMMERCE_MCP_SERVER_APPLICATION_NAME)
    
    # Register e-commerce tools
    logger.info("Registering E-commerce MCP tools...")
    
    browse_products_tool(mcp)
    get_category_counts_tool(mcp)
    
    # Register delivery tools
    logger.info("Registering Delivery Portal MCP tools...")
    
    get_delivery_routes_tool(mcp)
    get_orders_for_delivery_tool(mcp)
    get_delivery_slots_tool(mcp)
    get_delivery_drivers_tool(mcp)
    get_delivery_metrics_tool(mcp)
    
    # Register super admin tools
    logger.info("Registering Super Admin Portal MCP tools...")
    
    get_user_management_tool(mcp)
    get_system_health_tool(mcp)
    get_business_analytics_tool(mcp)
    get_security_audit_tool(mcp)
    get_system_config_tool(mcp)
    
    # Register supplier tools
    logger.info("Registering Supplier Portal MCP tools...")
    
    get_supplier_management_tool(mcp)
    get_purchase_orders_tool(mcp)
    get_invoice_management_tool(mcp)
    get_supplier_analytics_tool(mcp)
    get_product_catalog_tool(mcp)
    
    # Register warehouse management tools
    logger.info("Registering Warehouse Management Portal MCP tools...")
    
    get_inventory_management_tool(mcp)
    get_stock_movements_tool(mcp)
    get_warehouse_operations_tool(mcp)
    get_inventory_analytics_tool(mcp)
    get_quality_control_tool(mcp)
    
    # Note: Resource handlers removed for simplicity
    # The e-commerce tools are available directly via the registered @mcp.tool decorators
    logger.info("E-commerce, Delivery Portal, Super Admin Portal, Supplier Portal, and Warehouse Management Portal MCP Server initialized successfully")
    return mcp


async def main():
    """Main entry point for the MCP server."""
    
    # Configure logging
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.remove()  # Remove default handler
    logger.add(
        lambda msg: print(msg, end=""),
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    logger.info(f"Starting {ECOMMERCE_MCP_SERVER_APPLICATION_NAME}")
    
    # Log configuration information
    logger.info("E-commerce, Delivery Portal, Super Admin Portal, Supplier Portal, and Warehouse Management Portal MCP Server Configuration:")
    logger.info(f"  - Log Level: {log_level}")
    logger.info(f"  - AWS Region: {os.getenv('AWS_REGION', 'ap-south-1')}")
    
    # Create and run the server
    try:
        server = create_server()
        
        logger.info("E-commerce, Delivery Portal, Super Admin Portal, Supplier Portal, and Warehouse Management Portal MCP Server is ready to process requests")
        
        # Run the server in stdio mode for MCP communication
        logger.info("Starting MCP server in stdio mode...")
        await server.run_stdio_async()
        
    except KeyboardInterrupt:
        logger.info("Shutting down E-commerce and Delivery Portal MCP Server...")
    except Exception as e:
        logger.error(f"Error running E-commerce and Delivery Portal MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main()) 