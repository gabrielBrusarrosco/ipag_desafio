from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.api.v1.schemas import customer as customer_schemas

class CustomerRepository:
    @staticmethod
    def get_or_create(db: Session, customer_data: customer_schemas.OrderCustomer) -> Customer:
        db_customer = db.query(Customer).filter(Customer.document == customer_data.document).first()
        if db_customer:
            return db_customer

        db_customer = Customer(**customer_data.model_dump())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer