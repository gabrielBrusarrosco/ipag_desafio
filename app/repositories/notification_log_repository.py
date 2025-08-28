# app/repositories/notification_log_repository.py

from sqlalchemy.orm import Session
from app.models.notification_log import NotificationLog
from app.models.order import Order

class NotificationLogRepository:
    @staticmethod
    def create_log(db: Session, log_data: dict) -> NotificationLog:
        log_data.pop("user_id", None)
        log_data.pop("timestamp", None)

        db_log = NotificationLog(**log_data)
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log