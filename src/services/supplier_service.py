"""
Supplier Service - Supplier management and procurement operations.
"""

import boto3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from decimal import Decimal

from loguru import logger

from ..models.supplier_models import (
    SupplierManagementRequest, PurchaseOrderRequest, InvoiceManagementRequest,
    SupplierAnalyticsRequest, ProductCatalogRequest,
    SupplierManagementResult, PurchaseOrderResult, InvoiceManagementResult,
    SupplierAnalyticsResult, ProductCatalogResult,
    SupplierInfo, PurchaseOrder, Invoice, SupplierProduct, SupplierMetrics, ProcurementData
)


class SupplierService:
    """Service for supplier management and procurement operations."""

    def __init__(self, region_name: str = None):
        """Initialize the supplier service."""
        self.region_name = region_name or os.getenv('AWS_REGION', 'ap-south-1')
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        
        # Initialize table references
        suppliers_table_name = os.getenv('SUPPLIERS_TABLE_NAME', 'AuroraSparkTheme-Suppliers')
        orders_table_name = os.getenv('ORDERS_TABLE_NAME', 'AuroraSparkTheme-Orders')
        products_table_name = os.getenv('PRODUCTS_TABLE_NAME', 'AuroraSparkTheme-Products')
        procurement_table_name = os.getenv('PROCUREMENT_TABLE_NAME', 'AuroraSparkTheme-Procurement')
        
        self.suppliers_table = self.dynamodb.Table(suppliers_table_name)
        self.orders_table = self.dynamodb.Table(orders_table_name)
        self.products_table = self.dynamodb.Table(products_table_name)
        self.procurement_table = self.dynamodb.Table(procurement_table_name)

    async def manage_suppliers(self, request: SupplierManagementRequest) -> SupplierManagementResult:
        """Manage suppliers - get, filter, and manage supplier accounts."""
        try:
            logger.info(f"Managing suppliers - Category: {request.category}, Status: {request.status}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.category:
                filter_conditions.append('category = :category')
                expression_values[':category'] = request.category.lower()
            
            if request.status:
                filter_conditions.append('status = :status')
                expression_values[':status'] = request.status.lower()
            
            if request.search_term:
                filter_conditions.append('contains(companyName, :search_term) OR contains(contactPerson, :search_term)')
                expression_values[':search_term'] = request.search_term.lower()
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query suppliers
            if filter_expression:
                response = self.suppliers_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.suppliers_table.scan(Limit=max_results)
            
            # Process results
            suppliers = []
            for item in response.get('Items', []):
                supplier = self._process_raw_supplier(item)
                if supplier:
                    suppliers.append(supplier)
            
            total_found = response.get('Count', 0)
            returned_count = len(suppliers)
            
            logger.info(f"Found {total_found} suppliers, returning {returned_count}")
            
            return SupplierManagementResult(
                status="success",
                suppliers=suppliers,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing suppliers: {str(e)}")
            return SupplierManagementResult(
                status="error",
                error_message=str(e),
                suppliers=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    async def manage_purchase_orders(self, request: PurchaseOrderRequest) -> PurchaseOrderResult:
        """Manage purchase orders - get, filter, and track purchase orders."""
        try:
            logger.info(f"Managing purchase orders - Supplier: {request.supplier_id}, Status: {request.status}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.supplier_id:
                filter_conditions.append('supplierId = :supplier_id')
                expression_values[':supplier_id'] = request.supplier_id
            
            if request.status:
                filter_conditions.append('status = :status')
                expression_values[':status'] = request.status.lower()
            
            if request.date_from and request.date_to:
                filter_conditions.append('orderDate BETWEEN :date_from AND :date_to')
                expression_values[':date_from'] = request.date_from
                expression_values[':date_to'] = request.date_to
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query purchase orders
            if filter_expression:
                response = self.procurement_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.procurement_table.scan(Limit=max_results)
            
            # Process results
            orders = []
            for item in response.get('Items', []):
                order = self._process_raw_purchase_order(item)
                if order:
                    orders.append(order)
            
            total_found = response.get('Count', 0)
            returned_count = len(orders)
            
            logger.info(f"Found {total_found} purchase orders, returning {returned_count}")
            
            return PurchaseOrderResult(
                status="success",
                orders=orders,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing purchase orders: {str(e)}")
            return PurchaseOrderResult(
                status="error",
                error_message=str(e),
                orders=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    async def manage_invoices(self, request: InvoiceManagementRequest) -> InvoiceManagementResult:
        """Manage invoices - get, filter, and track supplier invoices."""
        try:
            logger.info(f"Managing invoices - Supplier: {request.supplier_id}, Status: {request.status}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.supplier_id:
                filter_conditions.append('supplierId = :supplier_id')
                expression_values[':supplier_id'] = request.supplier_id
            
            if request.status:
                filter_conditions.append('status = :status')
                expression_values[':status'] = request.status.lower()
            
            if request.date_from and request.date_to:
                filter_conditions.append('invoiceDate BETWEEN :date_from AND :date_to')
                expression_values[':date_from'] = request.date_from
                expression_values[':date_to'] = request.date_to
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query invoices
            if filter_expression:
                response = self.procurement_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.procurement_table.scan(Limit=max_results)
            
            # Process results
            invoices = []
            for item in response.get('Items', []):
                invoice = self._process_raw_invoice(item)
                if invoice:
                    invoices.append(invoice)
            
            total_found = response.get('Count', 0)
            returned_count = len(invoices)
            
            logger.info(f"Found {total_found} invoices, returning {returned_count}")
            
            return InvoiceManagementResult(
                status="success",
                invoices=invoices,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error managing invoices: {str(e)}")
            return InvoiceManagementResult(
                status="error",
                error_message=str(e),
                invoices=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    async def get_supplier_analytics(self, request: SupplierAnalyticsRequest) -> SupplierAnalyticsResult:
        """Get supplier analytics and performance metrics."""
        try:
            logger.info(f"Getting supplier analytics - Supplier: {request.supplier_id}, Period: {request.date_from} to {request.date_to}")
            
            # Get date range
            end_date = request.date_to or datetime.now().strftime('%Y-%m-%d')
            start_date = request.date_from or (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            # Get supplier metrics
            metrics = await self._get_supplier_metrics(request.supplier_id, start_date, end_date)
            
            # Get procurement data
            procurement_data = await self._get_procurement_data(start_date, end_date)
            
            logger.info(f"Supplier analytics retrieved - {len(metrics)} suppliers analyzed")
            
            return SupplierAnalyticsResult(
                status="success",
                metrics=metrics,
                procurement_data=procurement_data,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error getting supplier analytics: {str(e)}")
            return SupplierAnalyticsResult(
                status="error",
                error_message=str(e),
                metrics=[],
                procurement_data=ProcurementData(
                    total_suppliers=0,
                    active_suppliers=0,
                    total_purchase_orders=0,
                    total_invoice_value=0.0,
                    average_lead_time=0.0,
                    top_suppliers=[],
                    category_breakdown={}
                ),
                timestamp=datetime.now().isoformat()
            )

    async def get_product_catalog(self, request: ProductCatalogRequest) -> ProductCatalogResult:
        """Get supplier product catalog."""
        try:
            logger.info(f"Getting product catalog - Supplier: {request.supplier_id}, Category: {request.category}")
            
            # Validate request parameters
            max_results = min(max(request.max_results, 1), 100)
            
            # Build query parameters
            filter_conditions = []
            expression_values = {}
            
            if request.supplier_id:
                filter_conditions.append('supplierId = :supplier_id')
                expression_values[':supplier_id'] = request.supplier_id
            
            if request.category:
                filter_conditions.append('category = :category')
                expression_values[':category'] = request.category.lower()
            
            if request.search_term:
                filter_conditions.append('contains(productName, :search_term)')
                expression_values[':search_term'] = request.search_term.lower()
            
            # Build filter expression
            filter_expression = ' AND '.join(filter_conditions) if filter_conditions else None
            
            # Query products
            if filter_expression:
                response = self.products_table.scan(
                    FilterExpression=filter_expression,
                    ExpressionAttributeValues=expression_values,
                    Limit=max_results
                )
            else:
                response = self.products_table.scan(Limit=max_results)
            
            # Process results
            products = []
            for item in response.get('Items', []):
                product = self._process_raw_supplier_product(item)
                if product:
                    products.append(product)
            
            total_found = response.get('Count', 0)
            returned_count = len(products)
            
            logger.info(f"Found {total_found} products, returning {returned_count}")
            
            return ProductCatalogResult(
                status="success",
                products=products,
                total_found=total_found,
                returned_count=returned_count,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error getting product catalog: {str(e)}")
            return ProductCatalogResult(
                status="error",
                error_message=str(e),
                products=[],
                total_found=0,
                returned_count=0,
                timestamp=datetime.now().isoformat()
            )

    # Helper methods
    def _process_raw_supplier(self, raw_supplier: Dict[str, Any]) -> Optional[SupplierInfo]:
        """Process raw supplier data from DynamoDB."""
        try:
            return SupplierInfo(
                supplier_id=raw_supplier.get('supplierId', ''),
                company_name=raw_supplier.get('companyName', ''),
                contact_person=raw_supplier.get('contactPerson', ''),
                email=raw_supplier.get('email', ''),
                phone=raw_supplier.get('phone', ''),
                address=raw_supplier.get('address', ''),
                city=raw_supplier.get('city', ''),
                state=raw_supplier.get('state', ''),
                pincode=raw_supplier.get('pincode', ''),
                category=raw_supplier.get('category', ''),
                status=raw_supplier.get('status', 'active'),
                rating=float(raw_supplier.get('rating', 0.0)),
                total_orders=int(raw_supplier.get('totalOrders', 0)),
                total_value=float(raw_supplier.get('totalValue', 0.0)),
                created_at=raw_supplier.get('createdAt', ''),
                last_order_date=raw_supplier.get('lastOrderDate'),
                payment_terms=raw_supplier.get('paymentTerms'),
                delivery_lead_time=raw_supplier.get('deliveryLeadTime')
            )
        except Exception as e:
            logger.error(f"Error processing supplier: {str(e)}")
            return None

    def _process_raw_purchase_order(self, raw_order: Dict[str, Any]) -> Optional[PurchaseOrder]:
        """Process raw purchase order data from DynamoDB."""
        try:
            return PurchaseOrder(
                order_id=raw_order.get('orderId', ''),
                supplier_id=raw_order.get('supplierId', ''),
                supplier_name=raw_order.get('supplierName', ''),
                order_date=raw_order.get('orderDate', ''),
                expected_delivery=raw_order.get('expectedDelivery', ''),
                status=raw_order.get('status', 'pending'),
                total_amount=float(raw_order.get('totalAmount', 0.0)),
                items=raw_order.get('items', []),
                payment_terms=raw_order.get('paymentTerms', ''),
                special_instructions=raw_order.get('specialInstructions'),
                created_by=raw_order.get('createdBy'),
                approved_by=raw_order.get('approvedBy')
            )
        except Exception as e:
            logger.error(f"Error processing purchase order: {str(e)}")
            return None

    def _process_raw_invoice(self, raw_invoice: Dict[str, Any]) -> Optional[Invoice]:
        """Process raw invoice data from DynamoDB."""
        try:
            total_amount = float(raw_invoice.get('totalAmount', 0.0))
            paid_amount = float(raw_invoice.get('paidAmount', 0.0))
            
            return Invoice(
                invoice_id=raw_invoice.get('invoiceId', ''),
                supplier_id=raw_invoice.get('supplierId', ''),
                supplier_name=raw_invoice.get('supplierName', ''),
                invoice_date=raw_invoice.get('invoiceDate', ''),
                due_date=raw_invoice.get('dueDate', ''),
                status=raw_invoice.get('status', 'pending'),
                total_amount=total_amount,
                paid_amount=paid_amount,
                remaining_amount=total_amount - paid_amount,
                purchase_order_id=raw_invoice.get('purchaseOrderId'),
                payment_method=raw_invoice.get('paymentMethod'),
                notes=raw_invoice.get('notes')
            )
        except Exception as e:
            logger.error(f"Error processing invoice: {str(e)}")
            return None

    def _process_raw_supplier_product(self, raw_product: Dict[str, Any]) -> Optional[SupplierProduct]:
        """Process raw supplier product data from DynamoDB."""
        try:
            return SupplierProduct(
                product_id=raw_product.get('productId', ''),
                supplier_id=raw_product.get('supplierId', ''),
                product_name=raw_product.get('productName', ''),
                category=raw_product.get('category', ''),
                unit_price=float(raw_product.get('unitPrice', 0.0)),
                minimum_order_quantity=int(raw_product.get('minimumOrderQuantity', 1)),
                available_quantity=int(raw_product.get('availableQuantity', 0)),
                unit=raw_product.get('unit', ''),
                description=raw_product.get('description'),
                specifications=raw_product.get('specifications'),
                is_active=raw_product.get('isActive', True)
            )
        except Exception as e:
            logger.error(f"Error processing supplier product: {str(e)}")
            return None

    async def _get_supplier_metrics(self, supplier_id: Optional[str], start_date: str, end_date: str) -> List[SupplierMetrics]:
        """Get supplier performance metrics."""
        try:
            # This would typically query multiple tables to calculate metrics
            # For now, return mock data
            return [
                SupplierMetrics(
                    supplier_id="supplier_001",
                    supplier_name="Fresh Produce Co.",
                    total_orders=25,
                    total_value=150000.0,
                    average_order_value=6000.0,
                    on_time_delivery_rate=95.5,
                    quality_rating=4.2,
                    payment_terms_compliance=98.0,
                    period=f"{start_date} to {end_date}",
                    growth_rate=12.5
                )
            ]
        except Exception:
            return []

    async def _get_procurement_data(self, start_date: str, end_date: str) -> ProcurementData:
        """Get procurement analytics data."""
        try:
            # This would typically query multiple tables to calculate procurement data
            # For now, return mock data
            return ProcurementData(
                total_suppliers=15,
                active_suppliers=12,
                total_purchase_orders=45,
                total_invoice_value=250000.0,
                average_lead_time=3.5,
                top_suppliers=[],
                category_breakdown={
                    "produce": 5,
                    "dairy": 3,
                    "grains": 4,
                    "spices": 3
                }
            )
        except Exception:
            return ProcurementData(
                total_suppliers=0,
                active_suppliers=0,
                total_purchase_orders=0,
                total_invoice_value=0.0,
                average_lead_time=0.0,
                top_suppliers=[],
                category_breakdown={}
            )