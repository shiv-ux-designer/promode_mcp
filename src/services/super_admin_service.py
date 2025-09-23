"""
Super Admin Service - System administration and management operations.
"""

import boto3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from decimal import Decimal

from loguru import logger

from ..models.super_admin_models import (
    UserManagementRequest, SystemHealthRequest, AnalyticsRequest, SecurityAuditRequest,
    SystemConfigRequest, UserManagementResult, SystemHealthResult, AnalyticsResult,
    SecurityAuditResult, SystemConfigResult, AuditLogResult,
    UserInfo, SystemHealthStatus, BusinessMetrics, SecurityEvent, SystemConfiguration, AuditLog
)


class SuperAdminService:
    """Service for super admin operations and system management."""

    def __init__(self, region_name: str = None):
        """Initialize the super admin service."""
        self.region_name = region_name or os.getenv('AWS_REGION', 'ap-south-1')
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        
        # Initialize table references
        users_table_name = os.getenv('USERS_TABLE_NAME', 'AuroraSparkTheme-Users')
        orders_table_name = os.getenv('ORDERS_TABLE_NAME', 'AuroraSparkTheme-Orders')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME', 'AuroraSparkTheme-Products')
        analytics_table_name = os.getenv('ANALYTICS_TABLE_NAME', 'AuroraSparkTheme-Analytics')
        system_table_name = os.getenv('SYSTEM_TABLE_NAME', 'AuroraSparkTheme-System')
        
        self.users_table = self.dynamodb.Table(users_table_name)
        self.orders_table = self.dynamodb.Table(orders_table_name)
        self.products_table = self.dynamodb.Table(products_table_name)
        self.analytics_table = self.dynamodb.Table(analytics_table_name)
        self.system_table = self.dynamodb.Table(system_table_name)

    async def manage_users(self, request: UserManagementRequest) -> UserManagementResult:
        """Manage users - get, filter, and manage user accounts."""
        try:
            logger.info(f"Managing users - Type: {request.user_type}, Status: {request.status}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.user_type:
                filter_conditions.append('userType = :user_type')
                expression_values[':user_type'] = request.user_type.lower()
            
            if request.status:
                filter_conditions.append('status = :status')
                expression_values[':status'] = request.status.lower()
            
            if request.search_term:
                filter_conditions.append('contains(username, :search_term) OR contains(email, :search_term)')
                expression_values[':search_term'] = request.search_term.lower()
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query users
            if filter_expression:
                response = self.users_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.users_table.scan(Limit=max_results)
            
            # Process results
            users = []
            for item in response.get('Items', []):
                user = self._process_raw_user(item)
                if user:
                    users.append(user)
            
            total_found = response.get('Count', 0)
            returned_count = len(users)
            
            logger.info(f"Found {total_found} users, returning {returned_count}")
            
            return UserManagementResult(
                status="success",
                users=users,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing users: {str(e)}")
            return UserManagementResult(
                status="error",
                error_message=str(e),
                users=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    async def check_system_health(self, request: SystemHealthRequest) -> SystemHealthResult:
        """Check overall system health and status."""
        try:
            logger.info("Checking system health")
            
            # Check database connectivity
            db_status = "healthy"
            try:
                self.users_table.scan(Limit=1)
            except Exception as e:
                db_status = "error"
                logger.error(f"Database check failed: {e}")
            
            # Check AWS services
            aws_status = "healthy"
            try:
                # Test DynamoDB access
                self.analytics_table.scan(Limit=1)
            except Exception as e:
                aws_status = "error"
                logger.error(f"AWS services check failed: {e}")
            
            # Get system metrics
            active_users = await self._get_active_users_count()
            system_load = await self._get_system_load()
            uptime_percentage = await self._get_uptime_percentage()
            
            # Determine overall status
            if db_status == "healthy" and aws_status == "healthy":
                overall_status = "healthy"
            elif db_status == "error" or aws_status == "error":
                overall_status = "critical"
            else:
                overall_status = "warning"
            
            health_status = SystemHealthStatus(
                overall_status=overall_status,
                database_status=db_status,
                aws_services_status=aws_status,
                api_services_status="healthy",  # Assume healthy for now
                last_checked=datetime.now().isoformat(),
                uptime_percentage=uptime_percentage,
                active_users=active_users,
                system_load=system_load
            )
            
            logger.info(f"System health check completed - Status: {overall_status}")
            
            return SystemHealthResult(
                status="success",
                health_status=health_status,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error checking system health: {str(e)}")
            return SystemHealthResult(
                status="error",
                error_message=str(e),
                health_status=SystemHealthStatus(
                    overall_status="error",
                    database_status="error",
                    aws_services_status="error",
                    api_services_status="error",
                    last_checked=datetime.now().isoformat(),
                    uptime_percentage=0.0,
                    active_users=0,
                    system_load=0.0
                ),
                timestamp=datetime.now().isoformat()
            )

    async def get_business_analytics(self, request: AnalyticsRequest) -> AnalyticsResult:
        """Get business analytics and metrics."""
        try:
            logger.info(f"Getting business analytics - Period: {request.date_from} to {request.date_to}")
            
            # Get date range
            end_date = request.date_to or datetime.now().strftime('%Y-%m-%d')
            start_date = request.date_from or (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            # Get metrics from various tables
            total_revenue = await self._get_total_revenue(start_date, end_date)
            total_orders = await self._get_total_orders(start_date, end_date)
            total_users = await self._get_total_users()
            total_products = await self._get_total_products()
            
            # Calculate derived metrics
            average_order_value = total_revenue / total_orders if total_orders > 0 else 0
            conversion_rate = await self._get_conversion_rate(start_date, end_date)
            growth_rate = await self._get_growth_rate(start_date, end_date)
            
            metrics = BusinessMetrics(
                total_revenue=total_revenue,
                total_orders=total_orders,
                total_users=total_users,
                total_products=total_products,
                average_order_value=average_order_value,
                conversion_rate=conversion_rate,
                period=f"{start_date} to {end_date}",
                growth_rate=growth_rate
            )
            
            # Get chart data
            charts_data = await self._get_charts_data(start_date, end_date, request.group_by)
            
            logger.info(f"Business analytics retrieved - Revenue: {total_revenue}, Orders: {total_orders}")
            
            return AnalyticsResult(
                status="success",
                metrics=metrics,
                charts_data=charts_data,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error getting business analytics: {str(e)}")
            return AnalyticsResult(
                status="error",
                error_message=str(e),
                metrics=BusinessMetrics(
                    total_revenue=0.0,
                    total_orders=0,
                    total_users=0,
                    total_products=0,
                    average_order_value=0.0,
                    conversion_rate=0.0,
                    period="",
                    growth_rate=0.0
                ),
                charts_data={},
                timestamp=datetime.now().isoformat()
            )

    async def audit_security_events(self, request: SecurityAuditRequest) -> SecurityAuditResult:
        """Audit security events and activities."""
        try:
            logger.info(f"Auditing security events - Type: {request.audit_type}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.audit_type:
                filter_conditions.append('eventType = :audit_type')
                expression_values[':audit_type'] = request.audit_type.lower()
            
            if request.user_id:
                filter_conditions.append('userId = :user_id')
                expression_values[':user_id'] = request.user_id
            
            # Query security events (assuming they're stored in analytics table)
            if filter_conditions:
                filter_expression = ' AND '.join(filter_conditions)
                response = self.analytics_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.analytics_table.scan(Limit=max_results)
            
            # Process results
            events = []
            for item in response.get('Items', []):
                event = self._process_raw_security_event(item)
                if event:
                    events.append(event)
            
            total_found = response.get('Count', 0)
            returned_count = len(events)
            
            logger.info(f"Found {total_found} security events, returning {returned_count}")
            
            return SecurityAuditResult(
                status="success",
                events=events,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error auditing security events: {str(e)}")
            return SecurityAuditResult(
                status="error",
                error_message=str(e),
                events=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    async def manage_system_config(self, request: SystemConfigRequest) -> SystemConfigResult:
        """Manage system configuration settings."""
        try:
            logger.info(f"Managing system config - Type: {request.config_type}, Action: {request.action}")
            
            # Validate request parameters
            max_results = min(max(50, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.config_type:
                filter_conditions.append('configType = :config_type')
                expression_values[':config_type'] = request.config_type.lower()
            
            # Query system configurations
            if filter_conditions:
                filter_expression = ' AND '.join(filter_conditions)
                response = self.system_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.system_table.scan(Limit=max_results)
            
            # Process results
            configurations = []
            for item in response.get('Items', []):
                config = self._process_raw_system_config(item)
                if config:
                    configurations.append(config)
            
            total_found = response.get('Count', 0)
            returned_count = len(configurations)
            
            logger.info(f"Found {total_found} configurations, returning {returned_count}")
            
            return SystemConfigResult(
                status="success",
                configurations=configurations,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing system config: {str(e)}")
            return SystemConfigResult(
                status="error",
                error_message=str(e),
                configurations=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    # Helper methods
    def _process_raw_user(self, raw_user: Dict[str, Any]) -> Optional[UserInfo]:
        """Process raw user data from DynamoDB."""
        try:
            return UserInfo(
                user_id=raw_user.get('userId', ''),
                username=raw_user.get('username', ''),
                email=raw_user.get('email', ''),
                user_type=raw_user.get('userType', 'customer'),
                status=raw_user.get('status', 'active'),
                created_at=raw_user.get('createdAt', ''),
                last_login=raw_user.get('lastLogin'),
                phone=raw_user.get('phone'),
                address=raw_user.get('address'),
                permissions=raw_user.get('permissions', []),
                is_verified=raw_user.get('isVerified', False)
            )
        except Exception as e:
            logger.error(f"Error processing user: {str(e)}")
            return None

    def _process_raw_security_event(self, raw_event: Dict[str, Any]) -> Optional[SecurityEvent]:
        """Process raw security event data from DynamoDB."""
        try:
            return SecurityEvent(
                event_id=raw_event.get('eventId', ''),
                event_type=raw_event.get('eventType', ''),
                user_id=raw_event.get('userId'),
                timestamp=raw_event.get('timestamp', ''),
                ip_address=raw_event.get('ipAddress'),
                description=raw_event.get('description', ''),
                severity=raw_event.get('severity', 'low'),
                status=raw_event.get('status', 'pending')
            )
        except Exception as e:
            logger.error(f"Error processing security event: {str(e)}")
            return None

    def _process_raw_system_config(self, raw_config: Dict[str, Any]) -> Optional[SystemConfiguration]:
        """Process raw system configuration data from DynamoDB."""
        try:
            return SystemConfiguration(
                config_id=raw_config.get('configId', ''),
                config_type=raw_config.get('configType', ''),
                key=raw_config.get('key', ''),
                value=raw_config.get('value', ''),
                description=raw_config.get('description', ''),
                last_updated=raw_config.get('lastUpdated', ''),
                updated_by=raw_config.get('updatedBy', '')
            )
        except Exception as e:
            logger.error(f"Error processing system config: {str(e)}")
            return None

    async def _get_active_users_count(self) -> int:
        """Get count of active users."""
        try:
            response = self.users_table.scan(
                FilterExpression='status = :status',
                ExpressionAttributeValues={':status': 'active'}
            )
            return response.get('Count', 0)
        except Exception:
            return 0

    async def _get_system_load(self) -> float:
        """Get current system load percentage."""
        # This would typically come from system monitoring
        # For now, return a mock value
        return 45.5

    async def _get_uptime_percentage(self) -> float:
        """Get system uptime percentage."""
        # This would typically come from system monitoring
        # For now, return a mock value
        return 99.8

    async def _get_total_revenue(self, start_date: str, end_date: str) -> float:
        """Get total revenue for the period."""
        try:
            response = self.orders_table.scan(
                FilterExpression='orderDate BETWEEN :start_date AND :end_date',
                ExpressionAttributeValues={
                    ':start_date': start_date,
                    ':end_date': end_date
                }
            )
            
            total_revenue = 0.0
            for item in response.get('Items', []):
                total_revenue += float(item.get('totalAmount', 0))
            
            return total_revenue
        except Exception:
            return 0.0

    async def _get_total_orders(self, start_date: str, end_date: str) -> int:
        """Get total orders for the period."""
        try:
            response = self.orders_table.scan(
                FilterExpression='orderDate BETWEEN :start_date AND :end_date',
                ExpressionAttributeValues={
                    ':start_date': start_date,
                    ':end_date': end_date
                }
            )
            return response.get('Count', 0)
        except Exception:
            return 0

    async def _get_total_users(self) -> int:
        """Get total number of users."""
        try:
            response = self.users_table.scan()
            return response.get('Count', 0)
        except Exception:
            return 0

    async def _get_total_products(self) -> int:
        """Get total number of products."""
        try:
            response = self.products_table.scan()
            return response.get('Count', 0)
        except Exception:
            return 0

    async def _get_conversion_rate(self, start_date: str, end_date: str) -> float:
        """Get conversion rate for the period."""
        # This would typically be calculated from user behavior data
        # For now, return a mock value
        return 3.2

    async def _get_growth_rate(self, start_date: str, end_date: str) -> float:
        """Get growth rate for the period."""
        # This would typically be calculated from historical data
        # For now, return a mock value
        return 15.7

    async def _get_charts_data(self, start_date: str, end_date: str, group_by: Optional[str]) -> Dict[str, Any]:
        """Get chart data for analytics."""
        # This would typically generate various chart data
        # For now, return mock data
        return {
            "revenue_trend": [
                {"date": "2025-09-15", "revenue": 15000},
                {"date": "2025-09-16", "revenue": 18000},
                {"date": "2025-09-17", "revenue": 22000}
            ],
            "order_volume": [
                {"date": "2025-09-15", "orders": 45},
                {"date": "2025-09-16", "orders": 52},
                {"date": "2025-09-17", "orders": 61}
            ],
            "user_growth": [
                {"date": "2025-09-15", "users": 1200},
                {"date": "2025-09-16", "users": 1250},
                {"date": "2025-09-17", "users": 1300}
            ]
        }