import time
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.api.v1.schemas import order as order_schemas
import uuid
from fastapi import HTTPException
from typing import Optional
from app.core.messaging import RabbitMQPublisher

VALID_STATUS_TRANSITIONS = {
    "PENDING": ["WAITING_PAYMENT", "CANCELED"],
    "WAITING_PAYMENT": ["PAID", "CANCELED"],
    "PAID": ["PROCESSING", "CANCELED"],
    "PROCESSING": ["SHIPPED", "CANCELED"],
    "SHIPPED": ["DELIVERED"],
    "DELIVERED": [],
    "CANCELED": [],
}

class OrderService:
    @staticmethod
    def create_order(db: Session, order: order_schemas.OrderCreate):
        total_value = sum(item.quantity * item.unit_value for item in order.order.items)
        
        order_number = f"ORD-{int(time.time())}"
        
        order_data_for_repo = {
            "customer": order.customer,
            "items": order.order.items,
            "total_value": total_value,
            "order_number": order_number
        }


        return OrderRepository.create_order(db, order_data_for_repo)
    @staticmethod
    def get_by_id(db: Session, order_id: uuid.UUID):
        order = OrderRepository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    
    @staticmethod
    def list_all(db: Session, status: Optional[str] = None):
        return OrderRepository.list_all(db, status)
    
    @staticmethod
    def update_status(db: Session, order_id: uuid.UUID, status_update: order_schemas.OrderStatusUpdate):
        order = OrderRepository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        current_status = order.status
        new_status = status_update.status
        
        if new_status not in VALID_STATUS_TRANSITIONS.get(current_status, []):
            raise HTTPException(status_code=400, detail=f"Invalid status transition from {current_status} to {new_status}")
        
        updated_order = OrderRepository.update_status(db, order, new_status)
        
        publisher = RabbitMQPublisher()
        message = {
            "order_id": str(updated_order.id),
            "old_status": current_status,
            "new_status": new_status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_id": "system"
        }
        publisher.publish(message)
        publisher.close()

        return updated_order
    
    @staticmethod
    def get_summary(db: Session):
        summary_data = OrderRepository.get_summary(db)
        summary_data["total_revenue"] = summary_data["total_revenue"] or 0.0
        return summary_data