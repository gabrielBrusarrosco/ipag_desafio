from pydantic import BaseModel, Field, computed_field

class OrderItemBase(BaseModel):
    product_name: str = Field(..., max_length=100)
    quantity: int = Field(..., gt=0)
    unit_value: float = Field(..., gt=0)

class OrderItemResponse(OrderItemBase):
    @computed_field
    @property
    def total_value(self) -> float:
        return self.quantity * self.unit_value
    class Config:
        from_attributes = True