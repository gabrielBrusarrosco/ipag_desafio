from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from validate_docbr import CPF
import uuid

class OrderCustomer(BaseModel):
    id: Optional[uuid.UUID] = None
    name: str = Field(..., max_length=100)
    document: str
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)

    @field_validator("document")
    @classmethod
    def validate_document_as_cpf(cls, v: str) -> str:
        cpf_validator = CPF()
        if not cpf_validator.validate(v):
            raise ValueError("CPF fornecido é inválido.")
        return "".join(filter(str.isdigit, v))
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        return "".join(filter(str.isdigit, v))

class CustomerResponse(OrderCustomer):
    id: uuid.UUID
    class Config:
        from_attributes = True