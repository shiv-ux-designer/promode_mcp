"""Warehouse Management tools for the Warehouse Management Portal MCP Server."""

import os
from datetime import datetime
from typing import Dict, List, Optional

from loguru import logger
from mcp.server.fastmcp import FastMCP

from ..models.warehouse_models import (
    InventoryManagementRequest, StockMovementRequest, WarehouseOperationsRequest,
    InventoryAnalyticsRequest, QualityControlRequest,
    InventoryManagementResult, StockMovementResult, WarehouseOperationsResult,
    InventoryAnalyticsResult, QualityControlResult
)
from ..services.warehouse_service import WarehouseService


def get_inventory_management_tool(mcp: FastMCP) -> None:
    """Register the inventory management tool."""
    
    @mcp.tool(description="Manage inventory - view, filter, and track inventory items across warehouses")
    async def get_inventory_management(
        product_id: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        warehouse_id: Optional[str] = None,
        search_term: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Manage inventory across warehouses.
        
        Args:
            product_id: Filter by specific product ID
            category: Filter by product category
            status: Filter by inventory status (in_stock, low_stock, out_of_stock, discontinued)
            warehouse_id: Filter by specific warehouse ID
            search_term: Search in product names
            max_results: Maximum number of items to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - inventory_items: List of inventory items with details
            - total_found: Total number of items found
            - returned_count: Number of items returned
        """
        try:
            logger.info(f"Managing inventory - Category: {category}, Status: {status}, Warehouse: {warehouse_id}")
            
            # Create inventory management request
            request = InventoryManagementRequest(
                product_id=product_id,
                category=category,
                status=status,
                warehouse_id=warehouse_id,
                search_term=search_term,
                max_results=max_results
            )
            
            # Initialize service and get inventory
            service = WarehouseService()
            result = await service.manage_inventory(request)
            
            # Convert result to dictionary format
            response = _convert_inventory_management_result_to_dict(result)
            logger.info(f"Inventory management completed - Found {result.total_found} items")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing inventory: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "inventory_items": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_stock_movements_tool(mcp: FastMCP) -> None:
    """Register the stock movements management tool."""
    
    @mcp.tool(description="Manage stock movements - view, filter, and track stock movements and transfers")
    async def get_stock_movements(
        movement_id: Optional[str] = None,
        product_id: Optional[str] = None,
        movement_type: Optional[str] = None,
        warehouse_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Manage stock movements and transfers.
        
        Args:
            movement_id: Filter by specific movement ID
            product_id: Filter by product ID
            movement_type: Filter by movement type (inbound, outbound, transfer, adjustment)
            warehouse_id: Filter by warehouse ID
            date_from: Start date for movements (YYYY-MM-DD format)
            date_to: End date for movements (YYYY-MM-DD format)
            max_results: Maximum number of movements to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - movements: List of stock movements with details
            - total_found: Total number of movements found
            - returned_count: Number of movements returned
        """
        try:
            logger.info(f"Managing stock movements - Type: {movement_type}, Product: {product_id}")
            
            # Create stock movement request
            request = StockMovementRequest(
                movement_id=movement_id,
                product_id=product_id,
                movement_type=movement_type,
                warehouse_id=warehouse_id,
                date_from=date_from,
                date_to=date_to,
                max_results=max_results
            )
            
            # Initialize service and get movements
            service = WarehouseService()
            result = await service.manage_stock_movements(request)
            
            # Convert result to dictionary format
            response = _convert_stock_movement_result_to_dict(result)
            logger.info(f"Stock movements management completed - Found {result.total_found} movements")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing stock movements: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "movements": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_warehouse_operations_tool(mcp: FastMCP) -> None:
    """Register the warehouse operations management tool."""
    
    @mcp.tool(description="Manage warehouse operations - view, filter, and track warehouse activities and efficiency")
    async def get_warehouse_operations(
        warehouse_id: Optional[str] = None,
        operation_type: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Manage warehouse operations and activities.
        
        Args:
            warehouse_id: Filter by specific warehouse ID
            operation_type: Filter by operation type (receiving, picking, packing, shipping)
            status: Filter by operation status (pending, in_progress, completed, cancelled)
            date_from: Start date for operations (YYYY-MM-DD format)
            date_to: End date for operations (YYYY-MM-DD format)
            max_results: Maximum number of operations to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - operations: List of warehouse operations with details
            - total_found: Total number of operations found
            - returned_count: Number of operations returned
        """
        try:
            logger.info(f"Managing warehouse operations - Type: {operation_type}, Status: {status}")
            
            # Create warehouse operations request
            request = WarehouseOperationsRequest(
                warehouse_id=warehouse_id,
                operation_type=operation_type,
                status=status,
                date_from=date_from,
                date_to=date_to,
                max_results=max_results
            )
            
            # Initialize service and get operations
            service = WarehouseService()
            result = await service.manage_warehouse_operations(request)
            
            # Convert result to dictionary format
            response = _convert_warehouse_operations_result_to_dict(result)
            logger.info(f"Warehouse operations management completed - Found {result.total_found} operations")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing warehouse operations: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "operations": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_inventory_analytics_tool(mcp: FastMCP) -> None:
    """Register the inventory analytics tool."""
    
    @mcp.tool(description="Get inventory analytics and performance metrics")
    async def get_inventory_analytics(
        warehouse_id: Optional[str] = None,
        category: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        metric_type: Optional[str] = None
    ) -> Dict:
        """
        Get inventory analytics and performance metrics.
        
        Args:
            warehouse_id: Filter by specific warehouse ID
            category: Filter by product category
            date_from: Start date for analytics (YYYY-MM-DD format)
            date_to: End date for analytics (YYYY-MM-DD format)
            metric_type: Type of metrics (turnover, valuation, movement, efficiency)
            
        Returns:
            Dictionary containing:
            - analytics: Inventory analytics data
            - metrics: Performance metrics
        """
        try:
            logger.info(f"Getting inventory analytics - Warehouse: {warehouse_id}, Category: {category}")
            
            # Create inventory analytics request
            request = InventoryAnalyticsRequest(
                warehouse_id=warehouse_id,
                category=category,
                date_from=date_from,
                date_to=date_to,
                metric_type=metric_type
            )
            
            # Initialize service and get analytics
            service = WarehouseService()
            result = await service.get_inventory_analytics(request)
            
            # Convert result to dictionary format
            response = _convert_inventory_analytics_result_to_dict(result)
            logger.info(f"Inventory analytics retrieved - {result.analytics.metrics.total_products} products analyzed")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting inventory analytics: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "analytics": {
                    "metrics": {
                        "total_products": 0,
                        "total_value": 0.0,
                        "average_turnover": 0.0,
                        "stock_accuracy": 0.0,
                        "fill_rate": 0.0,
                        "warehouse_utilization": 0.0,
                        "period": "",
                        "top_moving_products": [],
                        "low_stock_alerts": 0
                    },
                    "category_breakdown": {},
                    "value_breakdown": {},
                    "movement_trends": [],
                    "warehouse_performance": []
                },
                "timestamp": datetime.now().isoformat()
            }


def get_quality_control_tool(mcp: FastMCP) -> None:
    """Register the quality control management tool."""
    
    @mcp.tool(description="Manage quality control - view, filter, and track quality control batches and inspections")
    async def get_quality_control(
        batch_id: Optional[str] = None,
        product_id: Optional[str] = None,
        status: Optional[str] = None,
        warehouse_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Manage quality control batches and inspections.
        
        Args:
            batch_id: Filter by specific batch ID
            product_id: Filter by product ID
            status: Filter by quality status (pending, passed, failed, rework)
            warehouse_id: Filter by warehouse ID
            date_from: Start date for quality checks (YYYY-MM-DD format)
            date_to: End date for quality checks (YYYY-MM-DD format)
            max_results: Maximum number of batches to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - batches: List of quality control batches with details
            - total_found: Total number of batches found
            - returned_count: Number of batches returned
        """
        try:
            logger.info(f"Managing quality control - Product: {product_id}, Status: {status}")
            
            # Create quality control request
            request = QualityControlRequest(
                batch_id=batch_id,
                product_id=product_id,
                status=status,
                warehouse_id=warehouse_id,
                date_from=date_from,
                date_to=date_to,
                max_results=max_results
            )
            
            # Initialize service and get quality batches
            service = WarehouseService()
            result = await service.manage_quality_control(request)
            
            # Convert result to dictionary format
            response = _convert_quality_control_result_to_dict(result)
            logger.info(f"Quality control management completed - Found {result.total_found} batches")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing quality control: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "batches": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


# Helper functions for converting results to dictionaries
def _convert_inventory_management_result_to_dict(result: InventoryManagementResult) -> Dict:
    """Convert InventoryManagementResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "inventory_items": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "inventory_items": [
            {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "category": item.category,
                "sku": item.sku,
                "current_stock": item.current_stock,
                "reserved_stock": item.reserved_stock,
                "available_stock": item.available_stock,
                "minimum_stock": item.minimum_stock,
                "maximum_stock": item.maximum_stock,
                "unit_cost": item.unit_cost,
                "total_value": item.total_value,
                "warehouse_id": item.warehouse_id,
                "warehouse_name": item.warehouse_name,
                "location": item.location,
                "status": item.status,
                "last_updated": item.last_updated,
                "supplier": item.supplier,
                "batch_number": item.batch_number,
                "expiry_date": item.expiry_date
            }
            for item in result.inventory_items
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }


def _convert_stock_movement_result_to_dict(result: StockMovementResult) -> Dict:
    """Convert StockMovementResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "movements": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "movements": [
            {
                "movement_id": movement.movement_id,
                "product_id": movement.product_id,
                "product_name": movement.product_name,
                "movement_type": movement.movement_type,
                "quantity": movement.quantity,
                "unit_cost": movement.unit_cost,
                "total_value": movement.total_value,
                "warehouse_id": movement.warehouse_id,
                "warehouse_name": movement.warehouse_name,
                "reference_number": movement.reference_number,
                "movement_date": movement.movement_date,
                "created_by": movement.created_by,
                "notes": movement.notes,
                "destination_warehouse": movement.destination_warehouse
            }
            for movement in result.movements
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }


def _convert_warehouse_operations_result_to_dict(result: WarehouseOperationsResult) -> Dict:
    """Convert WarehouseOperationsResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "operations": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "operations": [
            {
                "operation_id": operation.operation_id,
                "operation_type": operation.operation_type,
                "warehouse_id": operation.warehouse_id,
                "warehouse_name": operation.warehouse_name,
                "status": operation.status,
                "start_time": operation.start_time,
                "end_time": operation.end_time,
                "duration_minutes": operation.duration_minutes,
                "items_processed": operation.items_processed,
                "efficiency_score": operation.efficiency_score,
                "operator_id": operation.operator_id,
                "operator_name": operation.operator_name,
                "notes": operation.notes
            }
            for operation in result.operations
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }


def _convert_inventory_analytics_result_to_dict(result: InventoryAnalyticsResult) -> Dict:
    """Convert InventoryAnalyticsResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "analytics": {
                "metrics": {
                    "total_products": 0,
                    "total_value": 0.0,
                    "average_turnover": 0.0,
                    "stock_accuracy": 0.0,
                    "fill_rate": 0.0,
                    "warehouse_utilization": 0.0,
                    "period": "",
                    "top_moving_products": [],
                    "low_stock_alerts": 0
                },
                "category_breakdown": {},
                "value_breakdown": {},
                "movement_trends": [],
                "warehouse_performance": []
            },
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "analytics": {
            "metrics": {
                "total_products": result.analytics.metrics.total_products,
                "total_value": result.analytics.metrics.total_value,
                "average_turnover": result.analytics.metrics.average_turnover,
                "stock_accuracy": result.analytics.metrics.stock_accuracy,
                "fill_rate": result.analytics.metrics.fill_rate,
                "warehouse_utilization": result.analytics.metrics.warehouse_utilization,
                "period": result.analytics.metrics.period,
                "top_moving_products": result.analytics.metrics.top_moving_products,
                "low_stock_alerts": result.analytics.metrics.low_stock_alerts
            },
            "category_breakdown": result.analytics.category_breakdown,
            "value_breakdown": result.analytics.value_breakdown,
            "movement_trends": result.analytics.movement_trends,
            "warehouse_performance": result.analytics.warehouse_performance
        },
        "timestamp": result.timestamp
    }


def _convert_quality_control_result_to_dict(result: QualityControlResult) -> Dict:
    """Convert QualityControlResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "batches": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "batches": [
            {
                "batch_id": batch.batch_id,
                "product_id": batch.product_id,
                "product_name": batch.product_name,
                "supplier_id": batch.supplier_id,
                "supplier_name": batch.supplier_name,
                "batch_number": batch.batch_number,
                "quantity_received": batch.quantity_received,
                "quantity_checked": batch.quantity_checked,
                "quantity_passed": batch.quantity_passed,
                "quantity_failed": batch.quantity_failed,
                "quality_score": batch.quality_score,
                "status": batch.status,
                "checked_by": batch.checked_by,
                "checked_date": batch.checked_date,
                "warehouse_id": batch.warehouse_id,
                "notes": batch.notes
            }
            for batch in result.batches
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }