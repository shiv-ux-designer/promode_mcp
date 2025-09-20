"""
Data models for delivery portal functionality.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from decimal import Decimal


@dataclass
class DeliveryRouteRequest:
    """Request parameters for delivery route management."""
    route_id: Optional[str] = None
    driver_id: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = None
    max_results: int = 20


@dataclass
class OrderDeliveryRequest:
    """Request parameters for order delivery operations."""
    order_id: Optional[str] = None
    driver_id: Optional[str] = None
    status: Optional[str] = None
    date: Optional[str] = None
    max_results: int = 20


@dataclass
class DeliverySlotRequest:
    """Request parameters for delivery slot management."""
    pincode: Optional[str] = None
    date: Optional[str] = None
    time_slot: Optional[str] = None
    max_results: int = 20


@dataclass
class DriverInfo:
    """Driver information."""
    driver_id: str
    name: str
    phone: str
    email: str
    license_number: str
    vehicle_type: str
    vehicle_number: str
    status: str = "active"
    rating: float = 0.0
    total_deliveries: int = 0
    current_location: Optional[Dict[str, float]] = None


@dataclass
class DeliveryAddress:
    """Delivery address information."""
    street: str
    city: str
    state: str
    pincode: str
    landmark: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None


@dataclass
class OrderItem:
    """Order item information."""
    product_id: str
    product_name: str
    quantity: int
    unit: str
    price: float
    total_price: float


@dataclass
class OrderInfo:
    """Order information for delivery."""
    order_id: str
    order_number: str
    customer_name: str
    customer_phone: str
    customer_email: str
    delivery_address: DeliveryAddress
    items: List[OrderItem]
    total_amount: float
    payment_method: str
    payment_status: str
    special_instructions: Optional[str] = None
    priority: str = "normal"


@dataclass
class DeliverySlot:
    """Delivery slot information."""
    slot_id: str
    pincode: str
    time_slot: str
    slot_type: str
    delivery_charge: float
    max_orders: int
    current_orders: int
    is_active: bool = True
    available_capacity: int = 0


@dataclass
class DeliveryRoute:
    """Delivery route information."""
    route_id: str
    route_name: str
    driver_id: str
    driver_name: str
    vehicle_number: str
    date: str
    status: str
    total_orders: int
    completed_orders: int
    total_distance: float
    estimated_duration: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    orders: List[OrderInfo] = field(default_factory=list)


@dataclass
class DeliveryStatus:
    """Delivery status information."""
    order_id: str
    status: str
    timestamp: datetime
    location: Optional[Dict[str, float]] = None
    notes: Optional[str] = None
    driver_id: Optional[str] = None


@dataclass
class DeliveryProof:
    """Delivery proof information."""
    proof_id: str
    order_id: str
    proof_type: str  # signature, photo, otp
    proof_data: str
    timestamp: datetime
    driver_id: str


@dataclass
class PaymentCollection:
    """Payment collection information."""
    payment_id: str
    order_id: str
    amount: float
    method: str  # cod, card, upi
    status: str
    collected_at: datetime
    driver_id: str


@dataclass
class DeliveryMetrics:
    """Delivery performance metrics."""
    total_deliveries: int
    successful_deliveries: int
    failed_deliveries: int
    success_rate: float
    average_delivery_time: float
    total_distance: float
    total_earnings: float


@dataclass
class RouteMetadata:
    """Metadata about route operations."""
    route_id: Optional[str] = None
    driver_id: Optional[str] = None
    date_filter: Optional[str] = None
    status_filter: Optional[str] = None
    max_results: int = 20


@dataclass
class DeliveryRouteResult:
    """Result of delivery route operations."""
    status: str
    routes: List[DeliveryRoute]
    total_found: int
    returned_count: int
    metadata: RouteMetadata
    timestamp: datetime
    error_message: Optional[str] = None


@dataclass
class OrderDeliveryResult:
    """Result of order delivery operations."""
    status: str
    orders: List[OrderInfo]
    total_found: int
    returned_count: int
    metadata: RouteMetadata
    timestamp: datetime
    error_message: Optional[str] = None


@dataclass
class DeliverySlotResult:
    """Result of delivery slot operations."""
    status: str
    slots: List[DeliverySlot]
    total_found: int
    returned_count: int
    timestamp: datetime
    pincode: Optional[str] = None
    date: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class DriverResult:
    """Result of driver operations."""
    status: str
    drivers: List[DriverInfo]
    total_found: int
    returned_count: int
    timestamp: datetime
    error_message: Optional[str] = None


@dataclass
class DeliveryMetricsResult:
    """Result of delivery metrics operations."""
    status: str
    metrics: DeliveryMetrics
    timestamp: datetime
    driver_id: Optional[str] = None
    date_range: Optional[Dict[str, str]] = None
    error_message: Optional[str] = None