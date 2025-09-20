"""Delivery tools for the Delivery Portal MCP Server."""

import os
from datetime import datetime
from typing import Dict, List, Optional

from loguru import logger
from mcp.server.fastmcp import FastMCP

from ..models.delivery_models import (
    DeliveryRouteRequest, OrderDeliveryRequest, DeliverySlotRequest,
    DeliveryRouteResult, OrderDeliveryResult, DeliverySlotResult, DriverResult, DeliveryMetricsResult
)
from ..services.delivery_service import DeliveryService


def get_delivery_routes_tool(mcp: FastMCP) -> None:
    """Register the get delivery routes tool."""
    
    @mcp.tool(description="Get delivery routes with filtering capabilities for route management")
    async def get_delivery_routes(
        route_id: Optional[str] = None,
        driver_id: Optional[str] = None,
        date: Optional[str] = None,
        status: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Get delivery routes based on various filters.
        
        Args:
            route_id: Filter by specific route ID
            driver_id: Filter by driver ID
            date: Filter by route date (YYYY-MM-DD format)
            status: Filter by route status (planned, in_progress, completed, cancelled)
            max_results: Maximum number of routes to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - routes: List of delivery routes with details
            - total_found: Total number of routes found
            - returned_count: Number of routes returned
            - metadata: Filter and search information
        """
        try:
            logger.info(f"Getting delivery routes - Driver: {driver_id}, Date: {date}, Status: {status}")
            
            # Create route request
            request = DeliveryRouteRequest(
                route_id=route_id,
                driver_id=driver_id,
                date=date,
                status=status,
                max_results=max_results
            )
            
            # Initialize service and get routes
            service = DeliveryService()
            result = await service.get_delivery_routes(request)
            
            # Convert result to dictionary format
            response = _convert_route_result_to_dict(result)
            logger.info(f"Delivery routes retrieved successfully - Found {result.total_found} routes")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting delivery routes: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "routes": [],
                "total_found": 0,
                "returned_count": 0,
                "metadata": {
                    "route_id": route_id,
                    "driver_id": driver_id,
                    "date": date,
                    "status": status,
                    "max_results": max_results
                },
                "timestamp": datetime.now().isoformat()
            }


def get_orders_for_delivery_tool(mcp: FastMCP) -> None:
    """Register the get orders for delivery tool."""
    
    @mcp.tool(description="Get orders assigned for delivery with filtering capabilities")
    async def get_orders_for_delivery(
        order_id: Optional[str] = None,
        driver_id: Optional[str] = None,
        status: Optional[str] = None,
        date: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Get orders assigned for delivery based on various filters.
        
        Args:
            order_id: Filter by specific order ID
            driver_id: Filter by assigned driver ID
            status: Filter by order status (packed, out_for_delivery, delivered, failed_delivery)
            date: Filter by delivery date (YYYY-MM-DD format)
            max_results: Maximum number of orders to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - orders: List of orders with delivery details
            - total_found: Total number of orders found
            - returned_count: Number of orders returned
            - metadata: Filter and search information
        """
        try:
            logger.info(f"Getting orders for delivery - Driver: {driver_id}, Status: {status}, Date: {date}")
            
            # Create order delivery request
            request = OrderDeliveryRequest(
                order_id=order_id,
                driver_id=driver_id,
                status=status,
                date=date,
                max_results=max_results
            )
            
            # Initialize service and get orders
            service = DeliveryService()
            result = await service.get_orders_for_delivery(request)
            
            # Convert result to dictionary format
            response = _convert_order_result_to_dict(result)
            logger.info(f"Orders for delivery retrieved successfully - Found {result.total_found} orders")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting orders for delivery: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "orders": [],
                "total_found": 0,
                "returned_count": 0,
                "metadata": {
                    "order_id": order_id,
                    "driver_id": driver_id,
                    "status": status,
                    "date": date,
                    "max_results": max_results
                },
                "timestamp": datetime.now().isoformat()
            }


def get_delivery_slots_tool(mcp: FastMCP) -> None:
    """Register the get delivery slots tool."""
    
    @mcp.tool(description="Get available delivery slots for specific pincodes and dates")
    async def get_delivery_slots(
        pincode: Optional[str] = None,
        date: Optional[str] = None,
        time_slot: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Get delivery slots based on location and time filters.
        
        Args:
            pincode: Filter by delivery pincode
            date: Filter by delivery date (YYYY-MM-DD format)
            time_slot: Filter by specific time slot
            max_results: Maximum number of slots to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - slots: List of delivery slots with availability
            - total_found: Total number of slots found
            - returned_count: Number of slots returned
            - pincode: Filtered pincode
            - date: Filtered date
        """
        try:
            logger.info(f"Getting delivery slots - Pincode: {pincode}, Date: {date}, Time: {time_slot}")
            
            # Create delivery slot request
            request = DeliverySlotRequest(
                pincode=pincode,
                date=date,
                time_slot=time_slot,
                max_results=max_results
            )
            
            # Initialize service and get slots
            service = DeliveryService()
            result = await service.get_delivery_slots(request)
            
            # Convert result to dictionary format
            response = _convert_slot_result_to_dict(result)
            logger.info(f"Delivery slots retrieved successfully - Found {result.total_found} slots")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting delivery slots: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "slots": [],
                "total_found": 0,
                "returned_count": 0,
                "pincode": pincode,
                "date": date,
                "timestamp": datetime.now().isoformat()
            }


def get_delivery_drivers_tool(mcp: FastMCP) -> None:
    """Register the get delivery drivers tool."""
    
    @mcp.tool(description="Get delivery drivers with their information and status")
    async def get_delivery_drivers(
        driver_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict:
        """
        Get delivery drivers based on criteria.
        
        Args:
            driver_id: Filter by specific driver ID
            status: Filter by driver status (active, inactive, on_break, on_leave)
            
        Returns:
            Dictionary containing:
            - drivers: List of drivers with their information
            - total_found: Total number of drivers found
            - returned_count: Number of drivers returned
        """
        try:
            logger.info(f"Getting delivery drivers - ID: {driver_id}, Status: {status}")
            
            # Initialize service and get drivers
            service = DeliveryService()
            result = await service.get_drivers(driver_id=driver_id, status=status)
            
            # Convert result to dictionary format
            response = _convert_driver_result_to_dict(result)
            logger.info(f"Delivery drivers retrieved successfully - Found {result.total_found} drivers")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting delivery drivers: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "drivers": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_delivery_metrics_tool(mcp: FastMCP) -> None:
    """Register the get delivery metrics tool."""
    
    @mcp.tool(description="Get delivery performance metrics and statistics")
    async def get_delivery_metrics(
        driver_id: Optional[str] = None,
        days: int = 30
    ) -> Dict:
        """
        Get delivery performance metrics for analysis.
        
        Args:
            driver_id: Filter by specific driver ID (optional)
            days: Number of days to analyze (default: 30)
            
        Returns:
            Dictionary containing:
            - metrics: Delivery performance metrics
            - driver_id: Filtered driver ID
            - date_range: Analysis date range
        """
        try:
            logger.info(f"Getting delivery metrics - Driver: {driver_id}, Days: {days}")
            
            # Initialize service and get metrics
            service = DeliveryService()
            result = await service.get_delivery_metrics(driver_id=driver_id, days=days)
            
            # Convert result to dictionary format
            response = _convert_metrics_result_to_dict(result)
            logger.info(f"Delivery metrics retrieved successfully")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting delivery metrics: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "metrics": {
                    "total_deliveries": 0,
                    "successful_deliveries": 0,
                    "failed_deliveries": 0,
                    "success_rate": 0.0,
                    "average_delivery_time": 0.0,
                    "total_distance": 0.0,
                    "total_earnings": 0.0
                },
                "driver_id": driver_id,
                "date_range": None,
                "timestamp": datetime.now().isoformat()
            }


# Helper functions to convert results to dictionary format

def _convert_route_result_to_dict(result: DeliveryRouteResult) -> Dict:
    """Convert DeliveryRouteResult to dictionary format."""
    return {
        "status": result.status,
        "routes": [
            {
                "route_id": route.route_id,
                "route_name": route.route_name,
                "driver_id": route.driver_id,
                "driver_name": route.driver_name,
                "vehicle_number": route.vehicle_number,
                "date": route.date,
                "status": route.status,
                "total_orders": route.total_orders,
                "completed_orders": route.completed_orders,
                "total_distance": route.total_distance,
                "estimated_duration": route.estimated_duration,
                "start_time": route.start_time,
                "end_time": route.end_time,
                "progress_percentage": (route.completed_orders / route.total_orders * 100) if route.total_orders > 0 else 0
            }
            for route in result.routes
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "metadata": {
            "route_id": result.metadata.route_id,
            "driver_id": result.metadata.driver_id,
            "date_filter": result.metadata.date_filter,
            "status_filter": result.metadata.status_filter,
            "max_results": result.metadata.max_results
        },
        "timestamp": result.timestamp.isoformat(),
        "error_message": result.error_message
    }


def _convert_order_result_to_dict(result: OrderDeliveryResult) -> Dict:
    """Convert OrderDeliveryResult to dictionary format."""
    return {
        "status": result.status,
        "orders": [
            {
                "order_id": order.order_id,
                "order_number": order.order_number,
                "customer_name": order.customer_name,
                "customer_phone": order.customer_phone,
                "customer_email": order.customer_email,
                "delivery_address": {
                    "street": order.delivery_address.street,
                    "city": order.delivery_address.city,
                    "state": order.delivery_address.state,
                    "pincode": order.delivery_address.pincode,
                    "landmark": order.delivery_address.landmark,
                    "coordinates": order.delivery_address.coordinates
                },
                "items": [
                    {
                        "product_id": item.product_id,
                        "product_name": item.product_name,
                        "quantity": item.quantity,
                        "unit": item.unit,
                        "price": item.price,
                        "total_price": item.total_price
                    }
                    for item in order.items
                ],
                "total_amount": order.total_amount,
                "payment_method": order.payment_method,
                "payment_status": order.payment_status,
                "special_instructions": order.special_instructions,
                "priority": order.priority
            }
            for order in result.orders
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "metadata": {
            "order_id": result.metadata.route_id,  # Using route_id field for order_id
            "driver_id": result.metadata.driver_id,
            "date_filter": result.metadata.date_filter,
            "status_filter": result.metadata.status_filter,
            "max_results": result.metadata.max_results
        },
        "timestamp": result.timestamp.isoformat(),
        "error_message": result.error_message
    }


def _convert_slot_result_to_dict(result: DeliverySlotResult) -> Dict:
    """Convert DeliverySlotResult to dictionary format."""
    return {
        "status": result.status,
        "slots": [
            {
                "slot_id": slot.slot_id,
                "pincode": slot.pincode,
                "time_slot": slot.time_slot,
                "slot_type": slot.slot_type,
                "delivery_charge": slot.delivery_charge,
                "max_orders": slot.max_orders,
                "current_orders": slot.current_orders,
                "is_active": slot.is_active,
                "available_capacity": slot.available_capacity,
                "capacity_percentage": (slot.available_capacity / slot.max_orders * 100) if slot.max_orders > 0 else 0
            }
            for slot in result.slots
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "pincode": result.pincode,
        "date": result.date,
        "timestamp": result.timestamp.isoformat(),
        "error_message": result.error_message
    }


def _convert_driver_result_to_dict(result: DriverResult) -> Dict:
    """Convert DriverResult to dictionary format."""
    return {
        "status": result.status,
        "drivers": [
            {
                "driver_id": driver.driver_id,
                "name": driver.name,
                "phone": driver.phone,
                "email": driver.email,
                "license_number": driver.license_number,
                "vehicle_type": driver.vehicle_type,
                "vehicle_number": driver.vehicle_number,
                "status": driver.status,
                "rating": driver.rating,
                "total_deliveries": driver.total_deliveries,
                "current_location": driver.current_location
            }
            for driver in result.drivers
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp.isoformat(),
        "error_message": result.error_message
    }


def _convert_metrics_result_to_dict(result: DeliveryMetricsResult) -> Dict:
    """Convert DeliveryMetricsResult to dictionary format."""
    return {
        "status": result.status,
        "metrics": {
            "total_deliveries": result.metrics.total_deliveries,
            "successful_deliveries": result.metrics.successful_deliveries,
            "failed_deliveries": result.metrics.failed_deliveries,
            "success_rate": result.metrics.success_rate,
            "average_delivery_time": result.metrics.average_delivery_time,
            "total_distance": result.metrics.total_distance,
            "total_earnings": result.metrics.total_earnings
        },
        "driver_id": result.driver_id,
        "date_range": result.date_range,
        "timestamp": result.timestamp.isoformat(),
        "error_message": result.error_message
    }