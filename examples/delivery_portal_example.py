"""
Delivery Portal Example - Demonstrates how to use the delivery portal MCP tools.

This example shows how to use the delivery portal tools to:
1. Get delivery routes
2. Get orders for delivery
3. Get delivery slots
4. Get delivery drivers
5. Get delivery metrics
"""

import asyncio
import os
from datetime import datetime

# Set up environment variables for AWS
os.environ['AWS_REGION'] = 'ap-south-1'
os.environ['ORDERS_TABLE_NAME'] = 'EcommerceApp-Orders'
os.environ['DELIVERY_TABLE_NAME'] = 'EcommerceApp-Delivery'
os.environ['LOGISTICS_TABLE_NAME'] = 'EcommerceApp-Logistics'
os.environ['STAFF_TABLE_NAME'] = 'EcommerceApp-Staff'

from src.services.delivery_service import DeliveryService
from src.models.delivery_models import (
    DeliveryRouteRequest, OrderDeliveryRequest, DeliverySlotRequest
)


async def main():
    """Main example function."""
    print("🚚 Delivery Portal Example")
    print("=" * 50)
    
    # Initialize delivery service
    delivery_service = DeliveryService()
    
    try:
        # 1. Get delivery routes
        print("\n1. Getting delivery routes...")
        route_request = DeliveryRouteRequest(
            driver_id="driver-001",
            date="2024-01-15",
            status="in_progress",
            max_results=10
        )
        routes_result = await delivery_service.get_delivery_routes(route_request)
        print(f"   Status: {routes_result.status}")
        print(f"   Found {routes_result.total_found} routes")
        for route in routes_result.routes[:3]:  # Show first 3 routes
            print(f"   - Route {route.route_id}: {route.route_name} ({route.status})")
            print(f"     Driver: {route.driver_name} | Orders: {route.completed_orders}/{route.total_orders}")
        
        # 2. Get orders for delivery
        print("\n2. Getting orders for delivery...")
        order_request = OrderDeliveryRequest(
            driver_id="driver-001",
            status="packed",
            date="2024-01-15",
            max_results=10
        )
        orders_result = await delivery_service.get_orders_for_delivery(order_request)
        print(f"   Status: {orders_result.status}")
        print(f"   Found {orders_result.total_found} orders")
        for order in orders_result.orders[:3]:  # Show first 3 orders
            print(f"   - Order {order.order_number}: {order.customer_name}")
            print(f"     Address: {order.delivery_address.street}, {order.delivery_address.city}")
            print(f"     Amount: ₹{order.total_amount} | Payment: {order.payment_method}")
        
        # 3. Get delivery slots
        print("\n3. Getting delivery slots...")
        slot_request = DeliverySlotRequest(
            pincode="560001",
            date="2024-01-15",
            max_results=10
        )
        slots_result = await delivery_service.get_delivery_slots(slot_request)
        print(f"   Status: {slots_result.status}")
        print(f"   Found {slots_result.total_found} slots")
        for slot in slots_result.slots[:3]:  # Show first 3 slots
            print(f"   - Slot {slot.slot_id}: {slot.time_slot}")
            print(f"     Type: {slot.slot_type} | Charge: ₹{slot.delivery_charge}")
            print(f"     Capacity: {slot.available_capacity}/{slot.max_orders}")
        
        # 4. Get delivery drivers
        print("\n4. Getting delivery drivers...")
        drivers_result = await delivery_service.get_drivers(status="active")
        print(f"   Status: {drivers_result.status}")
        print(f"   Found {drivers_result.total_found} drivers")
        for driver in drivers_result.drivers[:3]:  # Show first 3 drivers
            print(f"   - Driver {driver.driver_id}: {driver.name}")
            print(f"     Phone: {driver.phone} | Vehicle: {driver.vehicle_number}")
            print(f"     Rating: {driver.rating}/5 | Deliveries: {driver.total_deliveries}")
        
        # 5. Get delivery metrics
        print("\n5. Getting delivery metrics...")
        metrics_result = await delivery_service.get_delivery_metrics(driver_id="driver-001", days=30)
        print(f"   Status: {metrics_result.status}")
        if metrics_result.metrics:
            metrics = metrics_result.metrics
            print(f"   Total Deliveries: {metrics.total_deliveries}")
            print(f"   Successful: {metrics.successful_deliveries}")
            print(f"   Failed: {metrics.failed_deliveries}")
            print(f"   Success Rate: {metrics.success_rate:.1f}%")
            print(f"   Avg Delivery Time: {metrics.average_delivery_time} minutes")
            print(f"   Total Distance: {metrics.total_distance} km")
            print(f"   Total Earnings: ₹{metrics.total_earnings}")
        
        print("\n✅ Delivery Portal Example completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error in delivery portal example: {str(e)}")
        print("Note: This example requires proper AWS DynamoDB tables to be set up.")
        print("Make sure the following tables exist:")
        print("- EcommerceApp-Orders")
        print("- EcommerceApp-Delivery") 
        print("- EcommerceApp-Logistics")
        print("- EcommerceApp-Staff")


if __name__ == "__main__":
    asyncio.run(main())