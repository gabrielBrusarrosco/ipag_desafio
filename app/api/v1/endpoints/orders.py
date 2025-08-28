from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.v1.schemas import order as order_schemas
from app.services.order_service import OrderService
from app.core.database import SessionLocal
import uuid
from typing import Optional

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=order_schemas.OrderResponse, status_code=201)
def create_order(order_data: order_schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        created_order = OrderService.create_order(db, order_data)
        return created_order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/summary", response_model=order_schemas.OrderSummaryResponse)
def get_order_summary(db: Session = Depends(get_db)):
    summary = OrderService.get_summary(db)
    return summary

@router.get("/{order_id}", response_model=order_schemas.OrderResponse)
def get_order(order_id : uuid.UUID, db: Session = Depends(get_db)):
    db_order = OrderService.get_by_id(db, order_id)
    return db_order

@router.get("/", response_model=list[order_schemas.OrderResponse])
def list_orders(db: Session = Depends(get_db), status: Optional[str] = Query(None, description="Filtre os pedidos por status")):
    return OrderService.list_all(db=db, status=status)

@router.put("/{order_id}/status", response_model=order_schemas.OrderResponse)
def update_order_status(order_id: uuid.UUID, status_update: order_schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    try:
        return OrderService.update_status(db=db, order_id=order_id, status_update=status_update)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=400, detail=str(e))