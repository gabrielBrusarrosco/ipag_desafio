from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.messaging import RabbitMQPublisher
import pika

class HealthService:
    @staticmethod
    def check_database(db: Session):
        try:
            db.execute(text('SELECT 1'))
            return {"status": "ok"}
        except Exception:
            return {"status": "error"}

    @staticmethod
    def check_messaging():
        try:
            publisher = RabbitMQPublisher()
            publisher.close()
            return {"status": "ok"}
        except pika.exceptions.AMQPConnectionError:
            return {"status": "error"}

    @staticmethod
    def get_health_status(db: Session):
        db_status = HealthService.check_database(db)
        messaging_status = HealthService.check_messaging()

        health_status = {
            "api": {"status": "ok"},
            "database": db_status,
            "messaging": messaging_status
        }
        
        
        is_healthy = all(status['status'] == 'ok' for status in health_status.values())

        return health_status, is_healthy