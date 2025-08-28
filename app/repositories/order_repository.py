from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.customer_repository import CustomerRepository
import uuid
from typing import List, Optional

class OrderRepository:
    @staticmethod
    def create_order(db: Session, order_data: dict) -> Order:
        customer = CustomerRepository.get_or_create(db, order_data["customer"])

        db_order = Order(
            customer_id=customer.id,
            order_number=order_data["order_number"],
            total_value=order_data["total_value"],
            status="PENDING"
        )
        db.add(db_order)

        for item_data in order_data["items"]:
            db_item = OrderItem(
                order=db_order,
                product_name=item_data.product_name,
                quantity=item_data.quantity,
                unit_value=item_data.unit_value
            )
            db.add(db_item)

        db.commit()
        db.refresh(db_order)
        return db_order

    @staticmethod
    def get_by_id(db: Session, order_id: uuid.UUID) -> Order:
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def list_all(db: Session, status: Optional[str] = None) -> List[Order]:
        query = db.query(Order)
        if status:
            query = query.filter(Order.status == status)
        return query.order_by(Order.created_at.desc()).all()

    @staticmethod
    def update_status(db: Session, order: Order, new_status: str) -> Order:
        order.status = new_status
        db.commit()
        db.refresh(order)
        return order
    
    @staticmethod
    def get_summary(db: Session) -> dict:
        total_orders = db.query(func.count(Order.id)).scalar() or 0
        
        
        orders_by_status_query = db.query(
            Order.status, 
            func.count(Order.id)
        ).group_by(Order.status).all()
        
        
        orders_by_status = {status: count for status, count in orders_by_status_query}
        
        total_revenue = db.query(
            func.sum(Order.total_value)
        ).filter(Order.status == "PAID").scalar() or 0.0

        return {
            "total_orders": total_orders,
            "orders_by_status": orders_by_status,
            "total_revenue": total_revenue
        }