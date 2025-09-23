"""
Super Admin Portal Data Models - System administration and management models.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
from decimal import Decimal


# Request Models
@dataclass
class UserManagementRequest:
    """Request for user management operations."""
    user_id: Optional[str] = None
    user_type: Optional[str] = None  # customer, driver, supplier, admin
    status: Optional[str] = None  # active, inactive, suspended
    search_term: Optional[str] = None
    max_results: int = 20


@dataclass
class SystemHealthRequest:
    """Request for system health monitoring."""
    check_services: bool = True
    check_database: bool = True
    check_aws_services: bool = True


@dataclass
class AnalyticsRequest:
    """Request for business analytics."""
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    metric_type: Optional[str] = None  # sales, orders, users, inventory
    group_by: Optional[str] = None  # day, week, month, category


@dataclass
class SecurityAuditRequest:
    """Request for security audit operations."""
    audit_type: Optional[str] = None  # login_attempts, permissions, data_access
    user_id: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    max_results: int = 50


@dataclass
class SystemConfigRequest:
    """Request for system configuration management."""
    config_type: Optional[str] = None  # general, payment, delivery, notifications
    action: str = "get"  # get, set, update, delete


# Data Models
@dataclass
class UserInfo:
    """User information for admin management."""
    user_id: str
    username: str
    email: str
    user_type: str
    status: str
    created_at: str
    last_login: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    permissions: List[str] = None
    is_verified: bool = False


@dataclass
class SystemHealthStatus:
    """System health status information."""
    overall_status: str  # healthy, warning, critical
    database_status: str
    aws_services_status: str
    api_services_status: str
    last_checked: str
    uptime_percentage: float
    active_users: int
    system_load: float


@dataclass
class BusinessMetrics:
    """Business analytics metrics."""
    total_revenue: float
    total_orders: int
    total_users: int
    total_products: int
    average_order_value: float
    conversion_rate: float
    period: str
    growth_rate: float


@dataclass
class SecurityEvent:
    """Security audit event information."""
    event_id: str
    event_type: str
    user_id: Optional[str]
    timestamp: str
    ip_address: Optional[str]
    description: str
    severity: str  # low, medium, high, critical
    status: str  # resolved, pending, investigating


@dataclass
class SystemConfiguration:
    """System configuration settings."""
    config_id: str
    config_type: str
    key: str
    value: Any
    description: str
    last_updated: str
    updated_by: str


@dataclass
class AuditLog:
    """System audit log entry."""
    log_id: str
    action: str
    user_id: str
    resource_type: str
    resource_id: str
    timestamp: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None


# Result Models
@dataclass
class UserManagementResult:
    """Result of user management operations."""
    status: str
    users: List[UserInfo]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class SystemHealthResult:
    """Result of system health check."""
    status: str
    health_status: SystemHealthStatus
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class AnalyticsResult:
    """Result of analytics operations."""
    status: str
    metrics: BusinessMetrics
    charts_data: Dict[str, Any]
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class SecurityAuditResult:
    """Result of security audit operations."""
    status: str
    events: List[SecurityEvent]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class SystemConfigResult:
    """Result of system configuration operations."""
    status: str
    configurations: List[SystemConfiguration]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None


@dataclass
class AuditLogResult:
    """Result of audit log operations."""
    status: str
    logs: List[AuditLog]
    total_found: int
    returned_count: int
    timestamp: str
    error_message: Optional[str] = None