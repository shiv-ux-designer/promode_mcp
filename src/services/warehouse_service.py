"""
Warehouse Service - Inventory and warehouse management operations.
"""

import boto3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from decimal import Decimal

from loguru import logger

from ..models.warehouse_models import (
    InventoryManagementRequest, StockMovementRequest, WarehouseOperationsRequest,
    InventoryAnalyticsRequest, QualityControlRequest,
    InventoryManagementResult, StockMovementResult, WarehouseOperationsResult,
    InventoryAnalyticsResult, QualityControlResult,
    InventoryItem, StockMovement, WarehouseOperation, QualityControlBatch, WarehouseInfo, InventoryAnalytics, InventoryMetrics
)


class WarehouseService:
    """Service for warehouse and inventory management operations."""

    def __init__(self, region_name: str = None):
        """Initialize the warehouse service."""
        self.region_name = region_name or os.getenv('AWS_REGION', 'ap-south-1')
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        
        # Initialize table references
        inventory_table_name = os.getenv('INVENTORY_TABLE_NAME', 'AuroraSparkTheme-Inventory')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME', 'AuroraSparkTheme-Products')
        orders_table_name = os.getenv('ORDERS_TABLE_NAME', 'AuroraSparkTheme-Orders')
        quality_table_name = os.getenv('QUALITY_TABLE_NAME', 'AuroraSparkTheme-Quality')
        
        self.inventory_table = self.dynamodb.Table(inventory_table_name)
        self.products_table = self.dynamodb.Table(products_table_name)
        self.orders_table = self.dynamodb.Table(orders_table_name)
        self.quality_table = self.dynamodb.Table(quality_table_name)

    async def manage_inventory(self, request: InventoryManagementRequest) -> InventoryManagementResult:
        """Manage inventory - get, filter, and track inventory items."""
        try:
            logger.info(f"Managing inventory - Category: {request.category}, Status: {request.status}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.category:
                filter_conditions.append('category = :category')
                expression_values[':category'] = request.category.lower()
            
            if request.status:
                filter_conditions.append('status = :status')
                expression_values[':status'] = request.status.lower()
            
            if request.warehouse_id:
                filter_conditions.append('warehouseId = :warehouse_id')
                expression_values[':warehouse_id'] = request.warehouse_id
            
            if request.search_term:
                filter_conditions.append('contains(productName, :search_term)')
                expression_values[':search_term'] = request.search_term.lower()
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query inventory
            if filter_expression:
                response = self.inventory_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.inventory_table.scan(Limit=max_results)
            
            # Process results
            inventory_items = []
            for item in response.get('Items', []):
                inventory_item = self._process_raw_inventory_item(item)
                if inventory_item:
                    inventory_items.append(inventory_item)
            
            total_found = response.get('Count', 0)
            returned_count = len(inventory_items)
            
            logger.info(f"Found {total_found} inventory items, returning {returned_count}")
            
            return InventoryManagementResult(
                status="success",
                inventory_items=inventory_items,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing inventory: {str(e)}")
            return InventoryManagementResult(
                status="error",
                error_message=str(e),
                inventory_items=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    async def manage_stock_movements(self, request: StockMovementRequest) -> StockMovementResult:
        """Manage stock movements - get, filter, and track stock movements."""
        try:
            logger.info(f"Managing stock movements - Type: {request.movement_type}, Product: {request.product_id}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.product_id:
                filter_conditions.append('productId = :product_id')
                expression_values[':product_id'] = request.product_id
            
            if request.movement_type:
                filter_conditions.append('movementType = :movement_type')
                expression_values[':movement_type'] = request.movement_type.lower()
            
            if request.warehouse_id:
                filter_conditions.append('warehouseId = :warehouse_id')
                expression_values[':warehouse_id'] = request.warehouse_id
            
            if request.date_from and request.date_to:
                filter_conditions.append('movementDate BETWEEN :date_from AND :date_to')
                expression_values[':date_from'] = request.date_from
                expression_values[':date_to'] = request.date_to
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query stock movements
            if filter_expression:
                response = self.inventory_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.inventory_table.scan(Limit=max_results)
            
            # Process results
            movements = []
            for item in response.get('Items', []):
                movement = self._process_raw_stock_movement(item)
                if movement:
                    movements.append(movement)
            
            total_found = response.get('Count', 0)
            returned_count = len(movements)
            
            logger.info(f"Found {total_found} stock movements, returning {returned_count}")
            
            return StockMovementResult(
                status="success",
                movements=movements,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing stock movements: {str(e)}")
            return StockMovementResult(
                status="error",
                error_message=str(e),
                movements=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    async def manage_warehouse_operations(self, request: WarehouseOperationsRequest) -> WarehouseOperationsResult:
        """Manage warehouse operations - get, filter, and track warehouse operations."""
        try:
            logger.info(f"Managing warehouse operations - Type: {request.operation_type}, Status: {request.status}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.warehouse_id:
                filter_conditions.append('warehouseId = :warehouse_id')
                expression_values[':warehouse_id'] = request.warehouse_id
            
            if request.operation_type:
                filter_conditions.append('operationType = :operation_type')
                expression_values[':operation_type'] = request.operation_type.lower()
            
            if request.status:
                filter_conditions.append('status = :status')
                expression_values[':status'] = request.status.lower()
            
            if request.date_from and request.date_to:
                filter_conditions.append('startTime BETWEEN :date_from AND :date_to')
                expression_values[':date_from'] = request.date_from
                expression_values[':date_to'] = request.date_to
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query warehouse operations
            if filter_expression:
                response = self.inventory_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.inventory_table.scan(Limit=max_results)
            
            # Process results
            operations = []
            for item in response.get('Items', []):
                operation = self._process_raw_warehouse_operation(item)
                if operation:
                    operations.append(operation)
            
            total_found = response.get('Count', 0)
            returned_count = len(operations)
            
            logger.info(f"Found {total_found} warehouse operations, returning {returned_count}")
            
            return WarehouseOperationsResult(
                status="success",
                operations=operations,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing warehouse operations: {str(e)}")
            return WarehouseOperationsResult(
                status="error",
                error_message=str(e),
                operations=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    async def get_inventory_analytics(self, request: InventoryAnalyticsRequest) -> InventoryAnalyticsResult:
        """Get inventory analytics and performance metrics."""
        try:
            logger.info(f"Getting inventory analytics - Warehouse: {request.warehouse_id}, Category: {request.category}")
            
            # Get date range
            end_date = request.date_to or datetime.now().strftime('%Y-%m-%d')
            start_date = request.date_from or (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            # Get inventory metrics
            metrics = await self._get_inventory_metrics(request.warehouse_id, request.category, start_date, end_date)
            
            # Get analytics data
            analytics = await self._get_analytics_data(request.warehouse_id, request.category, start_date, end_date)
            
            logger.info(f"Inventory analytics retrieved - {metrics.total_products} products analyzed")
            
            return InventoryAnalyticsResult(
                status="success",
                analytics=analytics,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error getting inventory analytics: {str(e)}")
            return InventoryAnalyticsResult(
                status="error",
                error_message=str(e),
                analytics=InventoryAnalytics(
                    metrics=InventoryMetrics(
                        total_products=0,
                        total_value=0.0,
                        average_turnover=0.0,
                        stock_accuracy=0.0,
                        fill_rate=0.0,
                        warehouse_utilization=0.0,
                        period="",
                        top_moving_products=[],
                        low_stock_alerts=0
                    ),
                    category_breakdown={},
                    value_breakdown={},
                    movement_trends=[],
                    warehouse_performance=[]
                ),
                timestamp=datetime.now().isoformat()
            )

    async def manage_quality_control(self, request: QualityControlRequest) -> QualityControlResult:
        """Manage quality control - get, filter, and track quality control batches."""
        try:
            logger.info(f"Managing quality control - Product: {request.product_id}, Status: {request.status}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.product_id:
                filter_conditions.append('productId = :product_id')
                expression_values[':product_id'] = request.product_id
            
            if request.status:
                filter_conditions.append('status = :status')
                expression_values[':status'] = request.status.lower()
            
            if request.warehouse_id:
                filter_conditions.append('warehouseId = :warehouse_id')
                expression_values[':warehouse_id'] = request.warehouse_id
            
            if request.date_from and request.date_to:
                filter_conditions.append('checkedDate BETWEEN :date_from AND :date_to')
                expression_values[':date_from'] = request.date_from
                expression_values[':date_to'] = request.date_to
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query quality control batches
            if filter_expression:
                response = self.quality_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.quality_table.scan(Limit=max_results)
            
            # Process results
            batches = []
            for item in response.get('Items', []):
                batch = self._process_raw_quality_batch(item)
                if batch:
                    batches.append(batch)
            
            total_found = response.get('Count', 0)
            returned_count = len(batches)
            
            logger.info(f"Found {total_found} quality control batches, returning {returned_count}")
            
            return QualityControlResult(
                status="success",
                batches=batches,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing quality control: {str(e)}")
            return QualityControlResult(
                status="error",
                error_message=str(e),
                batches=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    # Helper methods
    def _process_raw_inventory_item(self, raw_item: Dict[str, Any]) -> Optional[InventoryItem]:
        """Process raw inventory item data from DynamoDB."""
        try:
            current_stock = int(raw_item.get('currentStock', 0))
            reserved_stock = int(raw_item.get('reservedStock', 0))
            unit_cost = float(raw_item.get('unitCost', 0.0))
            
            return InventoryItem(
                product_id=raw_item.get('productId', ''),
                product_name=raw_item.get('productName', ''),
                category=raw_item.get('category', ''),
                sku=raw_item.get('sku', ''),
                current_stock=current_stock,
                reserved_stock=reserved_stock,
                available_stock=current_stock - reserved_stock,
                minimum_stock=int(raw_item.get('minimumStock', 0)),
                maximum_stock=int(raw_item.get('maximumStock', 0)),
                unit_cost=unit_cost,
                total_value=current_stock * unit_cost,
                warehouse_id=raw_item.get('warehouseId', ''),
                warehouse_name=raw_item.get('warehouseName', ''),
                location=raw_item.get('location', ''),
                status=raw_item.get('status', 'in_stock'),
                last_updated=raw_item.get('lastUpdated', ''),
                supplier=raw_item.get('supplier'),
                batch_number=raw_item.get('batchNumber'),
                expiry_date=raw_item.get('expiryDate')
            )
        except Exception as e:
            logger.error(f"Error processing inventory item: {str(e)}")
            return None

    def _process_raw_stock_movement(self, raw_movement: Dict[str, Any]) -> Optional[StockMovement]:
        """Process raw stock movement data from DynamoDB."""
        try:
            return StockMovement(
                movement_id=raw_movement.get('movementId', ''),
                product_id=raw_movement.get('productId', ''),
                product_name=raw_movement.get('productName', ''),
                movement_type=raw_movement.get('movementType', ''),
                quantity=int(raw_movement.get('quantity', 0)),
                unit_cost=float(raw_movement.get('unitCost', 0.0)),
                total_value=float(raw_movement.get('totalValue', 0.0)),
                warehouse_id=raw_movement.get('warehouseId', ''),
                warehouse_name=raw_movement.get('warehouseName', ''),
                reference_number=raw_movement.get('referenceNumber', ''),
                movement_date=raw_movement.get('movementDate', ''),
                created_by=raw_movement.get('createdBy', ''),
                notes=raw_movement.get('notes'),
                destination_warehouse=raw_movement.get('destinationWarehouse')
            )
        except Exception as e:
            logger.error(f"Error processing stock movement: {str(e)}")
            return None

    def _process_raw_warehouse_operation(self, raw_operation: Dict[str, Any]) -> Optional[WarehouseOperation]:
        """Process raw warehouse operation data from DynamoDB."""
        try:
            return WarehouseOperation(
                operation_id=raw_operation.get('operationId', ''),
                operation_type=raw_operation.get('operationType', ''),
                warehouse_id=raw_operation.get('warehouseId', ''),
                warehouse_name=raw_operation.get('warehouseName', ''),
                status=raw_operation.get('status', 'pending'),
                start_time=raw_operation.get('startTime', ''),
                end_time=raw_operation.get('endTime'),
                duration_minutes=raw_operation.get('durationMinutes'),
                items_processed=int(raw_operation.get('itemsProcessed', 0)),
                efficiency_score=raw_operation.get('efficiencyScore'),
                operator_id=raw_operation.get('operatorId', ''),
                operator_name=raw_operation.get('operatorName', ''),
                notes=raw_operation.get('notes')
            )
        except Exception as e:
            logger.error(f"Error processing warehouse operation: {str(e)}")
            return None

    def _process_raw_quality_batch(self, raw_batch: Dict[str, Any]) -> Optional[QualityControlBatch]:
        """Process raw quality control batch data from DynamoDB."""
        try:
            return QualityControlBatch(
                batch_id=raw_batch.get('batchId', ''),
                product_id=raw_batch.get('productId', ''),
                product_name=raw_batch.get('productName', ''),
                supplier_id=raw_batch.get('supplierId', ''),
                supplier_name=raw_batch.get('supplierName', ''),
                batch_number=raw_batch.get('batchNumber', ''),
                quantity_received=int(raw_batch.get('quantityReceived', 0)),
                quantity_checked=int(raw_batch.get('quantityChecked', 0)),
                quantity_passed=int(raw_batch.get('quantityPassed', 0)),
                quantity_failed=int(raw_batch.get('quantityFailed', 0)),
                quality_score=float(raw_batch.get('qualityScore', 0.0)),
                status=raw_batch.get('status', 'pending'),
                checked_by=raw_batch.get('checkedBy', ''),
                checked_date=raw_batch.get('checkedDate', ''),
                warehouse_id=raw_batch.get('warehouseId', ''),
                notes=raw_batch.get('notes')
            )
        except Exception as e:
            logger.error(f"Error processing quality batch: {str(e)}")
            return None

    async def _get_inventory_metrics(self, warehouse_id: Optional[str], category: Optional[str], start_date: str, end_date: str) -> InventoryMetrics:
        """Get inventory performance metrics."""
        try:
            # This would typically query multiple tables to calculate metrics
            # For now, return mock data
            return InventoryMetrics(
                total_products=150,
                total_value=2500000.0,
                average_turnover=4.2,
                stock_accuracy=98.5,
                fill_rate=95.8,
                warehouse_utilization=78.5,
                period=f"{start_date} to {end_date}",
                top_moving_products=[
                    {"product_id": "prod_001", "product_name": "Apples", "movement_count": 45},
                    {"product_id": "prod_002", "product_name": "Bananas", "movement_count": 38}
                ],
                low_stock_alerts=5
            )
        except Exception:
            return InventoryMetrics(
                total_products=0,
                total_value=0.0,
                average_turnover=0.0,
                stock_accuracy=0.0,
                fill_rate=0.0,
                warehouse_utilization=0.0,
                period="",
                top_moving_products=[],
                low_stock_alerts=0
            )

    async def _get_analytics_data(self, warehouse_id: Optional[str], category: Optional[str], start_date: str, end_date: str) -> InventoryAnalytics:
        """Get inventory analytics data."""
        try:
            # This would typically query multiple tables to calculate analytics
            # For now, return mock data
            metrics = await self._get_inventory_metrics(warehouse_id, category, start_date, end_date)
            
            return InventoryAnalytics(
                metrics=metrics,
                category_breakdown={
                    "fruits": 45,
                    "vegetables": 38,
                    "dairy": 25,
                    "grains": 20
                },
                value_breakdown={
                    "fruits": 850000.0,
                    "vegetables": 720000.0,
                    "dairy": 480000.0,
                    "grains": 450000.0
                },
                movement_trends=[
                    {"date": "2025-09-15", "inbound": 120, "outbound": 95},
                    {"date": "2025-09-16", "inbound": 135, "outbound": 110},
                    {"date": "2025-09-17", "inbound": 150, "outbound": 125}
                ],
                warehouse_performance=[
                    {"warehouse_id": "wh_001", "warehouse_name": "Main Warehouse", "efficiency": 95.5},
                    {"warehouse_id": "wh_002", "warehouse_name": "Cold Storage", "efficiency": 92.3}
                ]
            )
        except Exception:
            return InventoryAnalytics(
                metrics=InventoryMetrics(
                    total_products=0,
                    total_value=0.0,
                    average_turnover=0.0,
                    stock_accuracy=0.0,
                    fill_rate=0.0,
                    warehouse_utilization=0.0,
                    period="",
                    top_moving_products=[],
                    low_stock_alerts=0
                ),
                category_breakdown={},
                value_breakdown={},
                movement_trends=[],
                warehouse_performance=[]
            )