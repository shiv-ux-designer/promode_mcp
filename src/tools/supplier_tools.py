"""Supplier tools for the Supplier Portal MCP Server."""

import os
from datetime import datetime
from typing import Dict, List, Optional

from loguru import logger
from mcp.server.fastmcp import FastMCP

from ..models.supplier_models import (
    SupplierManagementRequest, PurchaseOrderRequest, InvoiceManagementRequest,
    SupplierAnalyticsRequest, ProductCatalogRequest,
    SupplierManagementResult, PurchaseOrderResult, InvoiceManagementResult,
    SupplierAnalyticsResult, ProductCatalogResult
)
from ..services.supplier_service import SupplierService


def get_supplier_management_tool(mcp: FastMCP) -> None:
    """Register the supplier management tool."""
    
    @mcp.tool(description="Manage suppliers - view, filter, and manage supplier accounts and relationships")
    async def get_supplier_management(
        supplier_id: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        search_term: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Manage suppliers across the platform.
        
        Args:
            supplier_id: Filter by specific supplier ID
            status: Filter by supplier status (active, inactive, suspended, pending)
            category: Filter by supplier category (produce, dairy, grains, etc.)
            search_term: Search in company name or contact person
            max_results: Maximum number of suppliers to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - suppliers: List of suppliers with details
            - total_found: Total number of suppliers found
            - returned_count: Number of suppliers returned
        """
        try:
            logger.info(f"Managing suppliers - Category: {category}, Status: {status}, Search: {search_term}")
            
            # Create supplier management request
            request = SupplierManagementRequest(
                supplier_id=supplier_id,
                status=status,
                category=category,
                search_term=search_term,
                max_results=max_results
            )
            
            # Initialize service and get suppliers
            service = SupplierService()
            result = await service.manage_suppliers(request)
            
            # Convert result to dictionary format
            response = _convert_supplier_management_result_to_dict(result)
            logger.info(f"Supplier management completed - Found {result.total_found} suppliers")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing suppliers: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "suppliers": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_purchase_orders_tool(mcp: FastMCP) -> None:
    """Register the purchase orders management tool."""
    
    @mcp.tool(description="Manage purchase orders - view, filter, and track purchase orders with suppliers")
    async def get_purchase_orders(
        order_id: Optional[str] = None,
        supplier_id: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Manage purchase orders with suppliers.
        
        Args:
            order_id: Filter by specific order ID
            supplier_id: Filter by supplier ID
            status: Filter by order status (pending, approved, shipped, delivered, cancelled)
            date_from: Start date for orders (YYYY-MM-DD format)
            date_to: End date for orders (YYYY-MM-DD format)
            max_results: Maximum number of orders to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - orders: List of purchase orders with details
            - total_found: Total number of orders found
            - returned_count: Number of orders returned
        """
        try:
            logger.info(f"Managing purchase orders - Supplier: {supplier_id}, Status: {status}")
            
            # Create purchase order request
            request = PurchaseOrderRequest(
                order_id=order_id,
                supplier_id=supplier_id,
                status=status,
                date_from=date_from,
                date_to=date_to,
                max_results=max_results
            )
            
            # Initialize service and get orders
            service = SupplierService()
            result = await service.manage_purchase_orders(request)
            
            # Convert result to dictionary format
            response = _convert_purchase_order_result_to_dict(result)
            logger.info(f"Purchase orders management completed - Found {result.total_found} orders")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing purchase orders: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "orders": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_invoice_management_tool(mcp: FastMCP) -> None:
    """Register the invoice management tool."""
    
    @mcp.tool(description="Manage invoices - view, filter, and track supplier invoices and payments")
    async def get_invoice_management(
        invoice_id: Optional[str] = None,
        supplier_id: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Manage supplier invoices and payments.
        
        Args:
            invoice_id: Filter by specific invoice ID
            supplier_id: Filter by supplier ID
            status: Filter by invoice status (pending, paid, overdue, disputed)
            date_from: Start date for invoices (YYYY-MM-DD format)
            date_to: End date for invoices (YYYY-MM-DD format)
            max_results: Maximum number of invoices to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - invoices: List of invoices with details
            - total_found: Total number of invoices found
            - returned_count: Number of invoices returned
        """
        try:
            logger.info(f"Managing invoices - Supplier: {supplier_id}, Status: {status}")
            
            # Create invoice management request
            request = InvoiceManagementRequest(
                invoice_id=invoice_id,
                supplier_id=supplier_id,
                status=status,
                date_from=date_from,
                date_to=date_to,
                max_results=max_results
            )
            
            # Initialize service and get invoices
            service = SupplierService()
            result = await service.manage_invoices(request)
            
            # Convert result to dictionary format
            response = _convert_invoice_management_result_to_dict(result)
            logger.info(f"Invoice management completed - Found {result.total_found} invoices")
            
            return response
            
        except Exception as e:
            logger.error(f"Error managing invoices: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "invoices": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


def get_supplier_analytics_tool(mcp: FastMCP) -> None:
    """Register the supplier analytics tool."""
    
    @mcp.tool(description="Get supplier analytics and performance metrics")
    async def get_supplier_analytics(
        supplier_id: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        metric_type: Optional[str] = None,
        group_by: Optional[str] = None
    ) -> Dict:
        """
        Get supplier analytics and performance metrics.
        
        Args:
            supplier_id: Filter by specific supplier ID
            date_from: Start date for analytics (YYYY-MM-DD format)
            date_to: End date for analytics (YYYY-MM-DD format)
            metric_type: Type of metrics (performance, quality, delivery, cost)
            group_by: Group results by (month, quarter, year)
            
        Returns:
            Dictionary containing:
            - metrics: List of supplier performance metrics
            - procurement_data: Overall procurement analytics
        """
        try:
            logger.info(f"Getting supplier analytics - Supplier: {supplier_id}, Period: {date_from} to {date_to}")
            
            # Create supplier analytics request
            request = SupplierAnalyticsRequest(
                supplier_id=supplier_id,
                date_from=date_from,
                date_to=date_to,
                metric_type=metric_type,
                group_by=group_by
            )
            
            # Initialize service and get analytics
            service = SupplierService()
            result = await service.get_supplier_analytics(request)
            
            # Convert result to dictionary format
            response = _convert_supplier_analytics_result_to_dict(result)
            logger.info(f"Supplier analytics retrieved - {len(result.metrics)} suppliers analyzed")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting supplier analytics: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "metrics": [],
                "procurement_data": {
                    "total_suppliers": 0,
                    "active_suppliers": 0,
                    "total_purchase_orders": 0,
                    "total_invoice_value": 0.0,
                    "average_lead_time": 0.0,
                    "top_suppliers": [],
                    "category_breakdown": {}
                },
                "timestamp": datetime.now().isoformat()
            }


def get_product_catalog_tool(mcp: FastMCP) -> None:
    """Register the product catalog tool."""
    
    @mcp.tool(description="Get supplier product catalog and pricing information")
    async def get_product_catalog(
        supplier_id: Optional[str] = None,
        category: Optional[str] = None,
        search_term: Optional[str] = None,
        max_results: int = 20
    ) -> Dict:
        """
        Get supplier product catalog and pricing.
        
        Args:
            supplier_id: Filter by specific supplier ID
            category: Filter by product category
            search_term: Search in product names
            max_results: Maximum number of products to return (default: 20, max: 100)
            
        Returns:
            Dictionary containing:
            - products: List of supplier products with details
            - total_found: Total number of products found
            - returned_count: Number of products returned
        """
        try:
            logger.info(f"Getting product catalog - Supplier: {supplier_id}, Category: {category}")
            
            # Create product catalog request
            request = ProductCatalogRequest(
                supplier_id=supplier_id,
                category=category,
                search_term=search_term,
                max_results=max_results
            )
            
            # Initialize service and get products
            service = SupplierService()
            result = await service.get_product_catalog(request)
            
            # Convert result to dictionary format
            response = _convert_product_catalog_result_to_dict(result)
            logger.info(f"Product catalog retrieved - Found {result.total_found} products")
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting product catalog: {str(e)}")
            return {
                "status": "error",
                "error_message": str(e),
                "products": [],
                "total_found": 0,
                "returned_count": 0,
                "timestamp": datetime.now().isoformat()
            }


# Helper functions for converting results to dictionaries
def _convert_supplier_management_result_to_dict(result: SupplierManagementResult) -> Dict:
    """Convert SupplierManagementResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "suppliers": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "suppliers": [
            {
                "supplier_id": supplier.supplier_id,
                "company_name": supplier.company_name,
                "contact_person": supplier.contact_person,
                "email": supplier.email,
                "phone": supplier.phone,
                "address": supplier.address,
                "city": supplier.city,
                "state": supplier.state,
                "pincode": supplier.pincode,
                "category": supplier.category,
                "status": supplier.status,
                "rating": supplier.rating,
                "total_orders": supplier.total_orders,
                "total_value": supplier.total_value,
                "created_at": supplier.created_at,
                "last_order_date": supplier.last_order_date,
                "payment_terms": supplier.payment_terms,
                "delivery_lead_time": supplier.delivery_lead_time
            }
            for supplier in result.suppliers
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }


def _convert_purchase_order_result_to_dict(result: PurchaseOrderResult) -> Dict:
    """Convert PurchaseOrderResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "orders": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "orders": [
            {
                "order_id": order.order_id,
                "supplier_id": order.supplier_id,
                "supplier_name": order.supplier_name,
                "order_date": order.order_date,
                "expected_delivery": order.expected_delivery,
                "status": order.status,
                "total_amount": order.total_amount,
                "items": order.items,
                "payment_terms": order.payment_terms,
                "special_instructions": order.special_instructions,
                "created_by": order.created_by,
                "approved_by": order.approved_by
            }
            for order in result.orders
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }


def _convert_invoice_management_result_to_dict(result: InvoiceManagementResult) -> Dict:
    """Convert InvoiceManagementResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "invoices": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "invoices": [
            {
                "invoice_id": invoice.invoice_id,
                "supplier_id": invoice.supplier_id,
                "supplier_name": invoice.supplier_name,
                "invoice_date": invoice.invoice_date,
                "due_date": invoice.due_date,
                "status": invoice.status,
                "total_amount": invoice.total_amount,
                "paid_amount": invoice.paid_amount,
                "remaining_amount": invoice.remaining_amount,
                "purchase_order_id": invoice.purchase_order_id,
                "payment_method": invoice.payment_method,
                "notes": invoice.notes
            }
            for invoice in result.invoices
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }


def _convert_supplier_analytics_result_to_dict(result: SupplierAnalyticsResult) -> Dict:
    """Convert SupplierAnalyticsResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "metrics": [],
            "procurement_data": {
                "total_suppliers": 0,
                "active_suppliers": 0,
                "total_purchase_orders": 0,
                "total_invoice_value": 0.0,
                "average_lead_time": 0.0,
                "top_suppliers": [],
                "category_breakdown": {}
            },
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "metrics": [
            {
                "supplier_id": metric.supplier_id,
                "supplier_name": metric.supplier_name,
                "total_orders": metric.total_orders,
                "total_value": metric.total_value,
                "average_order_value": metric.average_order_value,
                "on_time_delivery_rate": metric.on_time_delivery_rate,
                "quality_rating": metric.quality_rating,
                "payment_terms_compliance": metric.payment_terms_compliance,
                "period": metric.period,
                "growth_rate": metric.growth_rate
            }
            for metric in result.metrics
        ],
        "procurement_data": {
            "total_suppliers": result.procurement_data.total_suppliers,
            "active_suppliers": result.procurement_data.active_suppliers,
            "total_purchase_orders": result.procurement_data.total_purchase_orders,
            "total_invoice_value": result.procurement_data.total_invoice_value,
            "average_lead_time": result.procurement_data.average_lead_time,
            "top_suppliers": [
                {
                    "supplier_id": supplier.supplier_id,
                    "supplier_name": supplier.supplier_name,
                    "total_orders": supplier.total_orders,
                    "total_value": supplier.total_value
                }
                for supplier in result.procurement_data.top_suppliers
            ],
            "category_breakdown": result.procurement_data.category_breakdown
        },
        "timestamp": result.timestamp
    }


def _convert_product_catalog_result_to_dict(result: ProductCatalogResult) -> Dict:
    """Convert ProductCatalogResult to dictionary format."""
    if result.status == "error":
        return {
            "status": result.status,
            "error_message": result.error_message,
            "products": [],
            "total_found": 0,
            "returned_count": 0,
            "timestamp": result.timestamp
        }
    
    return {
        "status": result.status,
        "products": [
            {
                "product_id": product.product_id,
                "supplier_id": product.supplier_id,
                "product_name": product.product_name,
                "category": product.category,
                "unit_price": product.unit_price,
                "minimum_order_quantity": product.minimum_order_quantity,
                "available_quantity": product.available_quantity,
                "unit": product.unit,
                "description": product.description,
                "specifications": product.specifications,
                "is_active": product.is_active
            }
            for product in result.products
        ],
        "total_found": result.total_found,
        "returned_count": result.returned_count,
        "timestamp": result.timestamp
    }