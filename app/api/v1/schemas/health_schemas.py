from pydantic import BaseModel

class HealthStatus(BaseModel):
    status: str = "ok"

class HealthCheckResponse(BaseModel):
    api: HealthStatus
    database: HealthStatus
    messaging: HealthStatus