"""Super Admin tools for the Super Admin Portal MCP Server."""

import os
from datetime import datetime
from typing import Dict, List, Optional

from loguru import logger
from mcp.server.fastmcp import FastMCP

from ..models.super_admin_models import (
    UserManagementRequest, SystemHealthRequest, AnalyticsRequest, SecurityAuditRequest,
    SystemConfigRequest, UserManagementResult, SystemHealthResult, AnalyticsResult,
    SecurityAuditResult, SystemConfigResult
)
from ..services.super_admin_service import SuperAdminService


def get_user_management_tool(mcp: FastMCP) -> None:
    """Register the user management tool."""
    
    @mcp.tool(description="Manage users - view, filter, and manage user accounts across the platform")
    async def get_user_management(
        user_id: Optional[str] = None,
        user_type: Optional[str] = None,
        status: Optional[str] = None,
        search_term: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Manage users across the platform.
        
        Args:
            user_id: Filter by specific user ID
            user_type: Filter by user type (customer, driver, supplier, admin)
            status: Filter by user status (active, inactive, suspended)
            search_term: Search in username or email
            max_results: Maximum number of users to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - users: List of users with details
            - total_found: Total number of users found
            - returned_count: Number of users returned
            - metadata: Filter and search information
        """
        try:
            logger.info(f"Managing users - Type: {user_type}, Status: {status}, Search: {search_term}")
            
            # Create user management request
            request = UserManagementRequest(
                user_id=user_id,
                user_type=user_type,
                status=status,
                search_term=search_term,
                max_results=max_results
            )
            
            # Initialize service and get users
            service = SuperAdminService()
            result = await service.manage_users(request)
            
            # Convert result to dictionary format
            response = _convert_user_management_result_to_dict(result)
            logger.info(f"User management completed - Found {result.total_found} users")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing users: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "users": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_system_health_tool(mcp: FastMCP) -> None:
    """Register the system health monitoring tool."""
    
    @mcp.tool(description="Check system health and monitor platform status")
    async def get_system_health(
        check_services: bool = True,
        check_database: bool = True,
        check_aws_services: bool = True
    ) -> Dict:
        """
        Check overall system health and status.
        
        Args:
            check_services: Check API services status
            check_database: Check database connectivity
            check_aws_services: Check AWS services status
            
        Returns:
            Dictionary containing:
            - health_status: Overall system health information
            - uptime_percentage: System uptime percentage
            - active_users: Number of active users
            - system_load: Current system load
        """
        try:
            logger.info("Checking system health")
            
            # Create system health request
            request = SystemHealthRequest(
                check_services=check_services,
                check_database=check_database,
                check_aws_services=check_aws_services
            )
            
            # Initialize service and check health
            service = SuperAdminService()
            result = await service.check_system_health(request)
            
            # Convert result to dictionary format
            response = _convert_system_health_result_to_dict(result)
            logger.info(f"System health check completed - Status: {result.health_status.overall_status}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error checking system health: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "health_status": {
                    "overall_status": "error",
                    "database_status": "error",
                    "aws_services_status": "error",
                    "api_services_status": "error",
                    "last_checked": datetime.now().isoformat(),
                    "uptime_percentage": 0.0,
                    "active_users": 0,
                    "system_load": 0.0
                },
                "timestamp": datetime.now().isoformat()
            }


def get_business_analytics_tool(mcp: FastMCP) -> None:
    """Register the business analytics tool."""
    
    @mcp.tool(description="Get business analytics and performance metrics")
    async def get_business_analytics(
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        metric_type: Optional[str] = None,
        group_by: Optional[str] = None
    ) -> Dict:
        """
        Get business analytics and performance metrics.
        
        Args:
            date_from: Start date for analytics (YYYY-MM-DD format)
            date_to: End date for analytics (YYYY-MM-DD format)
            metric_type: Type of metrics (sales, orders, users, inventory)
            group_by: Group results by (day, week, month, category)
            
        Returns:
            Dictionary containing:
            - metrics: Business performance metrics
            - charts_data: Data for charts and visualizations
            - period: Analytics period
        """
        try:
            logger.info(f"Getting business analytics - Period: {date_from} to {date_to}")
            
            # Create analytics request
            request = AnalyticsRequest(
                date_from=date_from,
                date_to=date_to,
                metric_type=metric_type,
                group_by=group_by
            )
            
            # Initialize service and get analytics
            service = SuperAdminService()
            result = await service.get_business_analytics(request)
            
            # Convert result to dictionary format
            response = _convert_analytics_result_to_dict(result)
            logger.info(f"Business analytics retrieved - Revenue: {result.metrics.total_revenue}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting business analytics: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "metrics": {
                    "total_revenue": 0.0,
                    "total_orders": 0,
                    "total_users": 0,
                    "total_products": 0,
                    "average_order_value": 0.0,
                    "conversion_rate": 0.0,
                    "period": "",
                    "growth_rate": 0.0
                },
                "charts_data": {},
                "timestamp": datetime.now().isoformat()
            }


def get_security_audit_tool(mcp: FastMCP) -> None:
    """Register the security audit tool."""
    
    @mcp.tool(description="Audit security events and monitor platform security")
    async def get_security_audit(
        audit_type: Optional[str] = None,
        user_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: int = 50
    ) -> Dict:
        """
        Audit security events and activities.
        
        Args:
            audit_type: Type of audit (login_attempts, permissions, data_access)
            user_id: Filter by specific user ID
            date_from: Start date for audit (YYYY-MM-DD format)
            date_to: End date for audit (YYYY-MM-DD format)
            max_results: Maximum number of events to return (default: 50, max: 100)
            
        Returns:
            Dictionary containing:
            - events: List of security events
            - total_found: Total number of events found
            - returned_count: Number of events returned
        """
        try:
            logger.info(f"Auditing security events - Type: {audit_type}, User: {user_id}")
            
            # Create security audit request
            request = SecurityAuditRequest(
                audit_type=audit_type,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                max_results=max_results
            )
            
            # Initialize service and audit security
            service = SuperAdminService()
            result = await service.audit_security_events(request)
            
            # Convert result to dictionary format
            response = _convert_security_audit_result_to_dict(result)
            logger.info(f"Security audit completed - Found {result.total_found} events")
            
            return response
            
        except Exception as e:
            logger.error(f"Error auditing security events: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "events": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_system_config_tool(mcp: FastMCP) -> None:
    """Register the system configuration management tool."""
    
    @mcp.tool(description="Manage system configuration settings and parameters")
    async def get_system_config(
        config_type: Optional[str] = None,
        action: str = "get"
    ) -> Dict:
        """
        Manage system configuration settings.
        
        Args:
            config_type: Type of configuration (general, payment, delivery, notifications)
            action: Action to perform (get, set, update, delete)
            
        Returns:
            Dictionary containing:
            - configurations: List of configuration settings
            - total_found: Total number of configurations found
            - returned_count: Number of configurations returned
        """
        try:
            logger.info(f"Managing system config - Type: {config_type}, Action: {action}")
            
            # Create system config request
            request = SystemConfigRequest(
                config_type=config_type,
                action=action
            )
            
            # Initialize service and manage config
            service = SuperAdminService()
            result = await service.manage_system_config(request)
            
            # Convert result to dictionary format
            response = _convert_system_config_result_to_dict(result)
            logger.info(f"System config management completed - Found {result.total_found} configurations")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing system config: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "configurations": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


# Helper functions for converting results to dictionaries
def _convert_user_management_result_to_dict(result: UserManagementResult) -> Dict:
    """Convert UserManagementResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "users": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "users": [
            {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
                "status": user.status,
                "created_at": user.created_at,
                "last_login": user.last_login,
                "phone": user.phone,
                "address": user.address,
                "permissions": user.permissions or [],
                "is_verified": user.is_verified
            }
            for user in result.users
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }


def _convert_system_health_result_to_dict(result: SystemHealthResult) -> Dict:
    """Convert SystemHealthResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "health_status": {
                "overall_status": "error",
                "database_status": "error",
                "aws_services_status": "error",
                "api_services_status": "error",
                "last_checked": result.timestamp,
                "uptime_percentage": 0.0,
                "active_users": 0,
                "system_load": 0.0
            },
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "health_status": {
            "overall_status": result.health_status.overall_status,
            "database_status": result.health_status.database_status,
            "aws_services_status": result.health_status.aws_services_status,
            "api_services_status": result.health_status.api_services_status,
            "last_checked": result.health_status.last_checked,
            "uptime_percentage": result.health_status.uptime_percentage,
            "active_users": result.health_status.active_users,
            "system_load": result.health_status.system_load
        },
        "timestamp": result.timestamp
    }


def _convert_analytics_result_to_dict(result: AnalyticsResult) -> Dict:
    """Convert AnalyticsResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "metrics": {
                "total_revenue": 0.0,
                "total_orders": 0,
                "total_users": 0,
                "total_products": 0,
                "average_order_value": 0.0,
                "conversion_rate": 0.0,
                "period": "",
                "growth_rate": 0.0
            },
            "charts_data": {},
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "metrics": {
            "total_revenue": result.metrics.total_revenue,
            "total_orders": result.metrics.total_orders,
            "total_users": result.metrics.total_users,
            "total_products": result.metrics.total_products,
            "average_order_value": result.metrics.average_order_value,
            "conversion_rate": result.metrics.conversion_rate,
            "period": result.metrics.period,
            "growth_rate": result.metrics.growth_rate
        },
        "charts_data": result.charts_data,
        "timestamp": result.timestamp
    }


def _convert_security_audit_result_to_dict(result: SecurityAuditResult) -> Dict:
    """Convert SecurityAuditResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "events": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "events": [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "user_id": event.user_id,
                "timestamp": event.timestamp,
                "ip_address": event.ip_address,
                "description": event.description,
                "severity": event.severity,
                "status": event.status
            }
            for event in result.events
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }


def _convert_system_config_result_to_dict(result: SystemConfigResult) -> Dict:
    """Convert SystemConfigResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "configurations": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "configurations": [
            {
                "config_id": config.config_id,
                "config_type": config.config_type,
                "key": config.key,
                "value": config.value,
                "description": config.description,
                "last_updated": config.last_updated,
                "updated_by": config.updated_by
            }
            for config in result.configurations
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }