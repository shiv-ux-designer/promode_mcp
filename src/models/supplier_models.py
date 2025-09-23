"""
Supplier Portal Data Models - Supplier management and procurement operations.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
from decimal import Decimal


# Request Models
@dataclass
class SupplierManagementRequest:
    """Request for supplier management operations."""
    supplier_id: Optional[str] = None
    status: Optional[str] = None  # active, inactive, suspended, pending
    category: Optional[str] = None  # produce, dairy, grains, etc.
    search_term: Optional[str] = None
    max_results: int = 20


@dataclass
class PurchaseOrderRequest:
    """Request for purchase order operations."""
    order_id: Optional[str] = None
    supplier_id: Optional[str] = None
    status: Optional[str] = None  # pending, approved, shipped, delivered, cancelled
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    max_results: int = 20


@dataclass
class InvoiceManagementRequest:
    """Request for invoice management operations."""
    invoice_id: Optional[str] = None
    supplier_id: Optional[str] = None
    status: Optional[str] = None  # pending, paid, overdue, disputed
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    max_results: int = 20


@dataclass
class SupplierAnalyticsRequest:
    """Request for supplier analytics."""
    supplier_id: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    metric_type: Optional[str] = None  # performance, quality, delivery, cost
    group_by: Optional[str] = None  # month, quarter, year


@dataclass
class ProductCatalogRequest:
    """Request for supplier product catalog."""
    supplier_id: Optional[str] = None
    category: Optional[str] = None
    search_term: Optional[str] = None
    max_results: int = 20


# Data Models
@dataclass
class SupplierInfo:
    """Supplier information for management."""
    supplier_id: str
    company_name: str
    contact_person: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    pincode: str
    category: str
    status: str
    rating: float
    total_orders: int
    total_value: float
    created_at: str
    last_order_date: Optional[str] = None
    payment_terms: Optional[str] = None
    delivery_lead_time: Optional[int] = None


@dataclass
class PurchaseOrder:
    """Purchase order information."""
    order_id: str
    supplier_id: str
    supplier_name: str
    order_date: str
    expected_delivery: str
    status: str
    total_amount: float
    items: List[Dict[str, Any]]
    payment_terms: str
    special_instructions: Optional[str] = None
    created_by: Optional[str] = None
    approved_by: Optional[str] = None


@dataclass
class Invoice:
    """Invoice information."""
    invoice_id: str
    supplier_id: str
    supplier_name: str
    invoice_date: str
    due_date: str
    status: str
    total_amount: float
    paid_amount: float
    remaining_amount: float
    purchase_order_id: Optional[str] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class SupplierProduct:
    """Supplier product information."""
    product_id: str
    supplier_id: str
    product_name: str
    category: str
    unit_price: float
    minimum_order_quantity: int
    available_quantity: int
    unit: str
    description: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None
    is_active: bool = True


@dataclass
class SupplierMetrics:
    """Supplier performance metrics."""
    supplier_id: str
    supplier_name: str
    total_orders: int
    total_value: float
    average_order_value: float
    on_time_delivery_rate: float
    quality_rating: float
    payment_terms_compliance: float
    period: str
    growth_rate: float


@dataclass
class ProcurementData:
    """Procurement analytics data."""
    total_suppliers: int
    active_suppliers: int
    total_purchase_orders: int
    total_invoice_value: float
    average_lead_time: float
    top_suppliers: List[SupplierMetrics]
    category_breakdown: Dict[str, int]


# Result Models
@dataclass
class SupplierManagementResult:
    """Result of supplier management operations."""
    status: str
    suppliers: List[SupplierInfo]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class PurchaseOrderResult:
    """Result of purchase order operations."""
    status: str
    orders: List[PurchaseOrder]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class InvoiceManagementResult:
    """Result of invoice management operations."""
    status: str
    invoices: List[Invoice]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class SupplierAnalyticsResult:
    """Result of supplier analytics operations."""
    status: str
    metrics: List[SupplierMetrics]
    procurement_data: ProcurementData
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class ProductCatalogResult:
    """Result of product catalog operations."""
    status: str
    products: List[SupplierProduct]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None