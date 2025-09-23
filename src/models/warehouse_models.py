"""
Warehouse Management Portal Data Models - Inventory and warehouse operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
from decimal import Decimal


# Request Models
@dataclass
class InventoryManagementRequest:
    """Request for inventory management operations."""
    product_id: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None  # in_stock, low_stock, out_of_stock, discontinued
    warehouse_id: Optional[str] = None
    search_term: Optional[str] = None
    max_results: int = 20


@dataclass
class StockMovementRequest:
    """Request for stock movement operations."""
    movement_id: Optional[str] = None
    product_id: Optional[str] = None
    movement_type: Optional[str] = None  # inbound, outbound, transfer, adjustment
    warehouse_id: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    max_results: int = 20


@dataclass
class WarehouseOperationsRequest:
    """Request for warehouse operations."""
    warehouse_id: Optional[str] = None
    operation_type: Optional[str] = None  # receiving, picking, packing, shipping
    status: Optional[str] = None  # pending, in_progress, completed, cancelled
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    max_results: int = 20


@dataclass
class InventoryAnalyticsRequest:
    """Request for inventory analytics."""
    warehouse_id: Optional[str] = None
    category: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    metric_type: Optional[str] = None  # turnover, valuation, movement, efficiency


@dataclass
class QualityControlRequest:
    """Request for quality control operations."""
    batch_id: Optional[str] = None
    product_id: Optional[str] = None
    status: Optional[str] = None  # pending, passed, failed, rework
    warehouse_id: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    max_results: int = 20


# Data Models
@dataclass
class InventoryItem:
    """Inventory item information."""
    product_id: str
    product_name: str
    category: str
    sku: str
    current_stock: int
    reserved_stock: int
    available_stock: int
    minimum_stock: int
    maximum_stock: int
    unit_cost: float
    total_value: float
    warehouse_id: str
    warehouse_name: str
    location: str
    status: str
    last_updated: str
    supplier: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[str] = None


@dataclass
class StockMovement:
    """Stock movement information."""
    movement_id: str
    product_id: str
    product_name: str
    movement_type: str
    quantity: int
    unit_cost: float
    total_value: float
    warehouse_id: str
    warehouse_name: str
    reference_number: str
    movement_date: str
    created_by: str
    notes: Optional[str] = None
    destination_warehouse: Optional[str] = None


@dataclass
class WarehouseOperation:
    """Warehouse operation information."""
    operation_id: str
    operation_type: str
    warehouse_id: str
    warehouse_name: str
    status: str
    start_time: str
    items_processed: int
    operator_id: str
    operator_name: str
    end_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    efficiency_score: Optional[float] = None
    notes: Optional[str] = None


@dataclass
class QualityControlBatch:
    """Quality control batch information."""
    batch_id: str
    product_id: str
    product_name: str
    supplier_id: str
    supplier_name: str
    batch_number: str
    quantity_received: int
    quantity_checked: int
    quantity_passed: int
    quantity_failed: int
    quality_score: float
    status: str
    checked_by: str
    checked_date: str
    warehouse_id: str
    notes: Optional[str] = None


@dataclass
class WarehouseInfo:
    """Warehouse information."""
    warehouse_id: str
    warehouse_name: str
    location: str
    city: str
    state: str
    pincode: str
    capacity: int
    current_utilization: float
    status: str
    manager_id: str
    manager_name: str
    contact_phone: str
    total_products: int
    total_value: float


@dataclass
class InventoryMetrics:
    """Inventory performance metrics."""
    total_products: int
    total_value: float
    average_turnover: float
    stock_accuracy: float
    fill_rate: float
    warehouse_utilization: float
    period: str
    top_moving_products: List[Dict[str, Any]]
    low_stock_alerts: int


@dataclass
class InventoryAnalytics:
    """Inventory analytics data."""
    metrics: InventoryMetrics
    category_breakdown: Dict[str, int]
    value_breakdown: Dict[str, float]
    movement_trends: List[Dict[str, Any]]
    warehouse_performance: List[Dict[str, Any]]


# Result Models
@dataclass
class InventoryManagementResult:
    """Result of inventory management operations."""
    status: str
    inventory_items: List[InventoryItem]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class StockMovementResult:
    """Result of stock movement operations."""
    status: str
    movements: List[StockMovement]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class WarehouseOperationsResult:
    """Result of warehouse operations."""
    status: str
    operations: List[WarehouseOperation]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class InventoryAnalyticsResult:
    """Result of inventory analytics operations."""
    status: str
    analytics: InventoryAnalytics
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class QualityControlResult:
    """Result of quality control operations."""
    status: str
    batches: List[QualityControlBatch]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None