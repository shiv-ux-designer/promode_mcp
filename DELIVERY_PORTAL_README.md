# 🚚 Delivery Portal - MCP Server

The Delivery Portal is a comprehensive Model Context Protocol (MCP) server that provides AI assistants with tools to manage delivery operations, logistics, and driver management for e-commerce platforms.

## 🏗️ Architecture

The Delivery Portal follows the same modular architecture as the main e-commerce MCP server:

```
src/
├── models/
│   └── delivery_models.py          # Data models for delivery operations
├── services/
│   └── delivery_service.py         # Business logic and DynamoDB operations
├── tools/
│   └── delivery_tools.py           # MCP tool definitions
└── server.py                       # Updated server with delivery tools
```

## 🛠️ Available Tools

### 1. **Get Delivery Routes** (`get_delivery_routes`)
Retrieve delivery routes with filtering capabilities.

**Parameters:**
- `route_id` (optional): Filter by specific route ID
- `driver_id` (optional): Filter by driver ID
- `date` (optional): Filter by route date (YYYY-MM-DD)
- `status` (optional): Filter by route status
- `max_results` (default: 20): Maximum routes to return

**Example Usage:**
```python
# Get all routes for a specific driver
routes = await get_delivery_routes(
    driver_id="driver-001",
    date="2024-01-15",
    status="in_progress"
)
```

### 2. **Get Orders for Delivery** (`get_orders_for_delivery`)
Retrieve orders assigned for delivery with filtering.

**Parameters:**
- `order_id` (optional): Filter by specific order ID
- `driver_id` (optional): Filter by assigned driver
- `status` (optional): Filter by order status
- `date` (optional): Filter by delivery date
- `max_results` (default: 20): Maximum orders to return

**Example Usage:**
```python
# Get packed orders for a driver
orders = await get_orders_for_delivery(
    driver_id="driver-001",
    status="packed",
    date="2024-01-15"
)
```

### 3. **Get Delivery Slots** (`get_delivery_slots`)
Retrieve available delivery slots for specific locations and times.

**Parameters:**
- `pincode` (optional): Filter by delivery pincode
- `date` (optional): Filter by delivery date
- `time_slot` (optional): Filter by specific time slot
- `max_results` (default: 20): Maximum slots to return

**Example Usage:**
```python
# Get available slots for a pincode
slots = await get_delivery_slots(
    pincode="560001",
    date="2024-01-15"
)
```

### 4. **Get Delivery Drivers** (`get_delivery_drivers`)
Retrieve delivery driver information and status.

**Parameters:**
- `driver_id` (optional): Filter by specific driver ID
- `status` (optional): Filter by driver status

**Example Usage:**
```python
# Get all active drivers
drivers = await get_delivery_drivers(status="active")
```

### 5. **Get Delivery Metrics** (`get_delivery_metrics`)
Retrieve delivery performance metrics and statistics.

**Parameters:**
- `driver_id` (optional): Filter by specific driver
- `days` (default: 30): Number of days to analyze

**Example Usage:**
```python
# Get metrics for a specific driver
metrics = await get_delivery_metrics(
    driver_id="driver-001",
    days=30
)
```

## 📊 Data Models

### Core Models

- **DeliveryRoute**: Route information with driver, orders, and status
- **OrderInfo**: Order details with customer info and delivery address
- **DeliverySlot**: Time slot availability and capacity
- **DriverInfo**: Driver details with performance metrics
- **DeliveryMetrics**: Performance statistics and KPIs

### Request/Response Models

- **DeliveryRouteRequest/Result**: Route query operations
- **OrderDeliveryRequest/Result**: Order delivery operations
- **DeliverySlotRequest/Result**: Slot availability operations
- **DriverResult**: Driver information operations
- **DeliveryMetricsResult**: Metrics and analytics operations

## 🗄️ Database Tables

The Delivery Portal expects the following DynamoDB tables:

1. **EcommerceApp-Orders**: Order information and delivery details
2. **EcommerceApp-Delivery**: Delivery slots and scheduling
3. **EcommerceApp-Logistics**: Route planning and management
4. **EcommerceApp-Staff**: Driver and personnel information

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
export AWS_REGION=ap-south-1
export ORDERS_TABLE_NAME=EcommerceApp-Orders
export DELIVERY_TABLE_NAME=EcommerceApp-Delivery
export LOGISTICS_TABLE_NAME=EcommerceApp-Logistics
export STAFF_TABLE_NAME=EcommerceApp-Staff
```

### 3. Run the Server
```bash
python -m src.server
```

### 4. Use with MCP Client
The delivery tools are automatically registered and available to MCP clients like Cursor IDE.

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all delivery portal tests
pytest tests/test_delivery_tools.py -v

# Run specific test class
pytest tests/test_delivery_tools.py::TestGetDeliveryRoutesTool -v

# Run with coverage
pytest tests/test_delivery_tools.py --cov=src.tools.delivery_tools
```

## 📝 Example Usage

See `examples/delivery_portal_example.py` for a complete working example that demonstrates all delivery portal functionality.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_REGION` | AWS region for DynamoDB | `ap-south-1` |
| `ORDERS_TABLE_NAME` | Orders table name | `EcommerceApp-Orders` |
| `DELIVERY_TABLE_NAME` | Delivery slots table | `EcommerceApp-Delivery` |
| `LOGISTICS_TABLE_NAME` | Routes table name | `EcommerceApp-Logistics` |
| `STAFF_TABLE_NAME` | Staff/Drivers table | `EcommerceApp-Staff` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🎯 Use Cases

### For Delivery Managers
- Monitor route progress and driver performance
- Assign orders to drivers based on location and capacity
- Track delivery metrics and success rates
- Manage delivery slots and availability

### For Drivers
- View assigned routes and orders
- Check delivery addresses and special instructions
- Update delivery status and collect payments
- Access performance metrics and ratings

### for AI Assistants
- Answer questions about delivery status
- Help customers track their orders
- Provide delivery estimates and slot availability
- Generate delivery reports and analytics

## 🔒 Security

- All operations use AWS IAM for authentication
- DynamoDB access is controlled through IAM policies
- Sensitive data like phone numbers and addresses are handled securely
- No direct database credentials are stored in code

## 📈 Performance

- Optimized DynamoDB queries with proper indexing
- Efficient data processing and filtering
- Minimal memory footprint for large datasets
- Async/await pattern for non-blocking operations

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add comprehensive tests for new functionality
3. Update documentation for any new features
4. Ensure all tests pass before submitting changes

## 📄 License

This project is licensed under the Apache License 2.0 - see the main project LICENSE file for details.