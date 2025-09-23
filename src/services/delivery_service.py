"""
Delivery Service - Delivery management and logistics operations for e-commerce platforms.
"""

import boto3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from decimal import Decimal

from loguru import logger

from ..models.delivery_models import (
    DeliveryRouteRequest, OrderDeliveryRequest, DeliverySlotRequest,
    DeliveryRouteResult, OrderDeliveryResult, DeliverySlotResult, DriverResult, DeliveryMetricsResult,
    DeliveryRoute, OrderInfo, DeliverySlot, DriverInfo, DeliveryMetrics, RouteMetadata
)


class DeliveryService:
    """Service for delivery and logistics operations."""

    def __init__(self, region_name: str = None):
        """Initialize the delivery service."""
        self.region_name = region_name or os.getenv('AWS_REGION', 'ap-south-1')
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        
        # Initialize table references
        orders_table_name = os.getenv('ORDERS_TABLE_NAME', 'AuroraSparkTheme-Orders')
        delivery_table_name = os.getenv('DELIVERY_TABLE_NAME', 'AuroraSparkTheme-Delivery')
        logistics_table_name = os.getenv('LOGISTICS_TABLE_NAME', 'AuroraSparkTheme-Logistics')
        staff_table_name = os.getenv('STAFF_TABLE_NAME', 'AuroraSparkTheme-Staff')
        
        self.orders_table = self.dynamodb.Table(orders_table_name)
        self.delivery_table = self.dynamodb.Table(delivery_table_name)
        self.logistics_table = self.dynamodb.Table(logistics_table_name)
        self.staff_table = self.dynamodb.Table(staff_table_name)

    async def get_delivery_routes(self, request: DeliveryRouteRequest) -> DeliveryRouteResult:
        """Get delivery routes based on request parameters."""
        try:
            logger.info(f"Getting delivery routes - Driver: {request.driver_id}, Date: {request.date}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.route_id:
                filter_conditions.append('routeID = :route_id')
                expression_values[':route_id'] = request.route_id
            
            if request.driver_id:
                filter_conditions.append('driverID = :driver_id')
                expression_values[':driver_id'] = request.driver_id
            
            if request.date:
                filter_conditions.append('routeDate = :date')
                expression_values[':date'] = request.date
            
            if request.status:
                filter_conditions.append('#status = :status')
                expression_values[':status'] = request.status
            
            # Query routes
            if filter_conditions:
                filter_expression = ' AND '.join(filter_conditions)
                response = self.logistics_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    ExpressionAttributeNames={'#status': 'status'}
                )
            else:
                response = self.logistics_table.scan()
            
            raw_routes = response.get('Items', [])
            
            # Process routes
            processed_routes = []
            for raw_route in raw_routes:
                route = self._process_raw_route(raw_route)
                if route:
                    processed_routes.append(route)
            
            # Sort by date and apply limit
            processed_routes.sort(key=lambda x: x.date, reverse=True)
            total_found = len(processed_routes)
            processed_routes = processed_routes[:max_results]
            
            # Create metadata
            metadata = RouteMetadata(
                route_id=request.route_id,
                driver_id=request.driver_id,
                date_filter=request.date,
                status_filter=request.status,
                max_results=max_results
            )
            
            return DeliveryRouteResult(
                status="success",
                routes=processed_routes,
                total_found=total_found,
                returned_count=len(processed_routes),
                metadata=metadata,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error getting delivery routes: {str(e)}")
            return DeliveryRouteResult(
                status="error",
                routes=[],
                total_found=0,
                returned_count=0,
                metadata=RouteMetadata(),
                timestamp=datetime.now(),
                error_message=str(e)
            )

    async def get_orders_for_delivery(self, request: OrderDeliveryRequest) -> OrderDeliveryResult:
        """Get orders for delivery based on request parameters."""
        try:
            logger.info(f"Getting orders for delivery - Driver: {request.driver_id}, Status: {request.status}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.order_id:
                filter_conditions.append('orderID = :order_id')
                expression_values[':order_id'] = request.order_id
            
            if request.driver_id:
                filter_conditions.append('assignedRider.riderID = :driver_id')
                expression_values[':driver_id'] = request.driver_id
            
            if request.status:
                filter_conditions.append('#status = :status')
                expression_values[':status'] = request.status
            
            if request.date:
                filter_conditions.append('deliveryDate = :date')
                expression_values[':date'] = request.date
            
            # Query orders
            if filter_conditions:
                filter_expression = ' AND '.join(filter_conditions)
                response = self.orders_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    ExpressionAttributeNames={'#status': 'status'}
                )
            else:
                response = self.orders_table.scan()
            
            raw_orders = response.get('Items', [])
            
            # Process orders
            processed_orders = []
            for raw_order in raw_orders:
                order = self._process_raw_order(raw_order)
                if order:
                    processed_orders.append(order)
            
            # Sort by delivery date and apply limit
            processed_orders.sort(key=lambda x: x.delivery_address.pincode)
            total_found = len(processed_orders)
            processed_orders = processed_orders[:max_results]
            
            # Create metadata
            metadata = RouteMetadata(
                driver_id=request.driver_id,
                date_filter=request.date,
                status_filter=request.status,
                max_results=max_results
            )
            
            return OrderDeliveryResult(
                status="success",
                orders=processed_orders,
                total_found=total_found,
                returned_count=len(processed_orders),
                metadata=metadata,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error getting orders for delivery: {str(e)}")
            return OrderDeliveryResult(
                status="error",
                orders=[],
                total_found=0,
                returned_count=0,
                metadata=RouteMetadata(),
                timestamp=datetime.now(),
                error_message=str(e)
            )

    async def get_delivery_slots(self, request: DeliverySlotRequest) -> DeliverySlotResult:
        """Get delivery slots based on request parameters."""
        try:
            logger.info(f"Getting delivery slots - Pincode: {request.pincode}, Date: {request.date}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.pincode:
                filter_conditions.append('pincodeID = :pincode')
                expression_values[':pincode'] = request.pincode
            
            if request.date:
                filter_conditions.append('slotDate = :date')
                expression_values[':date'] = request.date
            
            if request.time_slot:
                filter_conditions.append('timeSlot = :time_slot')
                expression_values[':time_slot'] = request.time_slot
            
            # Query delivery slots
            if filter_conditions:
                filter_expression = ' AND '.join(filter_conditions)
                response = self.delivery_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values
                )
            else:
                response = self.delivery_table.scan()
            
            raw_slots = response.get('Items', [])
            
            # Process slots
            processed_slots = []
            for raw_slot in raw_slots:
                slot = self._process_raw_slot(raw_slot)
                if slot:
                    processed_slots.append(slot)
            
            # Sort by time slot and apply limit
            processed_slots.sort(key=lambda x: x.time_slot)
            total_found = len(processed_slots)
            processed_slots = processed_slots[:max_results]
            
            return DeliverySlotResult(
                status="success",
                slots=processed_slots,
                total_found=total_found,
                returned_count=len(processed_slots),
                pincode=request.pincode,
                date=request.date,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error getting delivery slots: {str(e)}")
            return DeliverySlotResult(
                status="error",
                slots=[],
                total_found=0,
                returned_count=0,
                pincode=request.pincode,
                date=request.date,
                timestamp=datetime.now(),
                error_message=str(e)
            )

    async def get_drivers(self, driver_id: Optional[str] = None, status: Optional[str] = None) -> DriverResult:
        """Get delivery drivers based on criteria."""
        try:
            logger.info(f"Getting drivers - ID: {driver_id}, Status: {status}")
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if driver_id:
                filter_conditions.append('employeeID = :driver_id')
                expression_values[':driver_id'] = driver_id
            
            if status:
                filter_conditions.append('#status = :status')
                expression_values[':status'] = status
            
            # Add role filter for delivery personnel
            filter_conditions.append('contains(#roles, :role)')
            expression_values[':role'] = 'delivery_personnel'
            
            # Query staff table
            if filter_conditions:
                filter_expression = ' AND '.join(filter_conditions)
                response = self.staff_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    ExpressionAttributeNames={'#status': 'status', '#roles': 'roles'}
                )
            else:
                response = self.staff_table.scan()
            
            raw_drivers = response.get('Items', [])
            
            # Process drivers
            processed_drivers = []
            for raw_driver in raw_drivers:
                driver = self._process_raw_driver(raw_driver)
                if driver:
                    processed_drivers.append(driver)
            
            # Sort by name
            processed_drivers.sort(key=lambda x: x.name)
            
            return DriverResult(
                status="success",
                drivers=processed_drivers,
                total_found=len(processed_drivers),
                returned_count=len(processed_drivers),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error getting drivers: {str(e)}")
            return DriverResult(
                status="error",
                drivers=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now(),
                error_message=str(e)
            )

    async def get_delivery_metrics(self, driver_id: Optional[str] = None, days: int = 30) -> DeliveryMetricsResult:
        """Get delivery performance metrics."""
        try:
            logger.info(f"Getting delivery metrics - Driver: {driver_id}, Days: {days}")
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Build query for orders in date range
            filter_conditions = ['deliveryDate BETWEEN :start_date AND :end_date']
            expression_values = {
                ':start_date': start_date.date().isoformat(),
                ':end_date': end_date.date().isoformat()
            }
            
            if driver_id:
                filter_conditions.append('assignedRider.riderID = :driver_id')
                expression_values[':driver_id'] = driver_id
            
            # Query orders
            response = self.orders_table.scan(
                FilterExpression=' AND '.join(filter_conditions),
                ExpressionAttributeValues=expression_values
            )
            
            orders = response.get('Items', [])
            
            # Calculate metrics
            total_deliveries = len(orders)
            successful_deliveries = len([o for o in orders if o.get('status') == 'delivered'])
            failed_deliveries = len([o for o in orders if o.get('status') in ['failed_delivery', 'returned']])
            success_rate = (successful_deliveries / total_deliveries * 100) if total_deliveries > 0 else 0
            
            # Calculate average delivery time (simplified)
            average_delivery_time = 45.0  # minutes (would be calculated from actual data)
            
            # Calculate total distance (simplified)
            total_distance = total_deliveries * 5.0  # km (would be calculated from actual data)
            
            # Calculate total earnings (simplified)
            total_earnings = sum(float(o.get('orderSummary', {}).get('totalAmount', 0)) for o in orders if o.get('status') == 'delivered')
            
            metrics = DeliveryMetrics(
                total_deliveries=total_deliveries,
                successful_deliveries=successful_deliveries,
                failed_deliveries=failed_deliveries,
                success_rate=success_rate,
                average_delivery_time=average_delivery_time,
                total_distance=total_distance,
                total_earnings=total_earnings
            )
            
            return DeliveryMetricsResult(
                status="success",
                metrics=metrics,
                driver_id=driver_id,
                date_range={"start": start_date.date().isoformat(), "end": end_date.date().isoformat()},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error getting delivery metrics: {str(e)}")
            return DeliveryMetricsResult(
                status="error",
                metrics=DeliveryMetrics(0, 0, 0, 0.0, 0.0, 0.0, 0.0),
                timestamp=datetime.now(),
                error_message=str(e)
            )

    def _process_raw_route(self, raw_route: Dict[str, Any]) -> Optional[DeliveryRoute]:
        """Process raw route data from DynamoDB."""
        try:
            return DeliveryRoute(
                route_id=raw_route.get('routeID', ''),
                route_name=raw_route.get('routeName', 'Unnamed Route'),
                driver_id=raw_route.get('driverID', ''),
                driver_name=raw_route.get('driverName', 'Unknown Driver'),
                vehicle_number=raw_route.get('vehicleNumber', 'N/A'),
                date=raw_route.get('routeDate', ''),
                status=raw_route.get('status', 'unknown'),
                total_orders=raw_route.get('totalOrders', 0),
                completed_orders=raw_route.get('completedOrders', 0),
                total_distance=float(raw_route.get('totalDistance', 0)),
                estimated_duration=raw_route.get('estimatedDuration', 0),
                start_time=raw_route.get('actualStartTime'),
                end_time=raw_route.get('actualEndTime')
            )
        except Exception as e:
            logger.error(f"Error processing route: {str(e)}")
            return None

    def _process_raw_order(self, raw_order: Dict[str, Any]) -> Optional[OrderInfo]:
        """Process raw order data from DynamoDB."""
        try:
            # Process delivery address
            delivery_address_data = raw_order.get('deliveryAddress', {})
            delivery_address = DeliveryAddress(
                street=delivery_address_data.get('addressLine1', ''),
                city=delivery_address_data.get('city', ''),
                state=delivery_address_data.get('state', ''),
                pincode=delivery_address_data.get('pincode', ''),
                landmark=delivery_address_data.get('landmark')
            )
            
            # Process order items
            items = []
            for item_data in raw_order.get('items', []):
                item = OrderItem(
                    product_id=item_data.get('productID', ''),
                    product_name=item_data.get('name', ''),
                    quantity=item_data.get('quantity', 0),
                    unit=item_data.get('unit', 'piece'),
                    price=float(item_data.get('price', 0)),
                    total_price=float(item_data.get('total', 0))
                )
                items.append(item)
            
            return OrderInfo(
                order_id=raw_order.get('orderID', ''),
                order_number=raw_order.get('orderNumber', ''),
                customer_name=raw_order.get('customerInfo', {}).get('name', 'Unknown Customer'),
                customer_phone=raw_order.get('customerInfo', {}).get('phone', ''),
                customer_email=raw_order.get('customerEmail', ''),
                delivery_address=delivery_address,
                items=items,
                total_amount=float(raw_order.get('orderSummary', {}).get('totalAmount', 0)),
                payment_method=raw_order.get('paymentMethod', 'cod'),
                payment_status=raw_order.get('paymentStatus', 'pending'),
                special_instructions=raw_order.get('specialInstructions')
            )
        except Exception as e:
            logger.error(f"Error processing order: {str(e)}")
            return None

    def _process_raw_slot(self, raw_slot: Dict[str, Any]) -> Optional[DeliverySlot]:
        """Process raw slot data from DynamoDB."""
        try:
            slot_info = raw_slot.get('slotInfo', {})
            current_orders = int(slot_info.get('currentOrders', 0))
            max_orders = int(slot_info.get('maxOrders', 10))
            
            return DeliverySlot(
                slot_id=raw_slot.get('slotID', ''),
                pincode=raw_slot.get('pincodeID', ''),
                time_slot=slot_info.get('timeSlot', ''),
                slot_type=slot_info.get('slotType', 'standard'),
                delivery_charge=float(slot_info.get('deliveryCharge', 0)),
                max_orders=max_orders,
                current_orders=current_orders,
                is_active=slot_info.get('isActive', True),
                available_capacity=max_orders - current_orders
            )
        except Exception as e:
            logger.error(f"Error processing slot: {str(e)}")
            return None

    def _process_raw_driver(self, raw_driver: Dict[str, Any]) -> Optional[DriverInfo]:
        """Process raw driver data from DynamoDB."""
        try:
            personal_info = raw_driver.get('personalInfo', {})
            job_info = raw_driver.get('jobInfo', {})
            
            return DriverInfo(
                driver_id=raw_driver.get('employeeID', ''),
                name=f"{personal_info.get('firstName', '')} {personal_info.get('lastName', '')}".strip(),
                phone=personal_info.get('phone', ''),
                email=personal_info.get('email', ''),
                license_number=job_info.get('licenseNumber', ''),
                vehicle_type=job_info.get('vehicleType', 'bike'),
                vehicle_number=raw_driver.get('vehicleAssigned', 'N/A'),
                status=raw_driver.get('status', 'inactive'),
                rating=float(raw_driver.get('performance', {}).get('rating', 0)),
                total_deliveries=raw_driver.get('performance', {}).get('totalDeliveries', 0)
            )
        except Exception as e:
            logger.error(f"Error processing driver: {str(e)}")
            return None