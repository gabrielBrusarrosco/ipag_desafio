from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.v1.schemas import health_schemas
from app.services.health_service import HealthService
from .orders import get_db

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", response_model=health_schemas.HealthCheckResponse)
def health_check(db: Session = Depends(get_db)):
    health_status, is_healthy = HealthService.get_health_status(db)
    
    if not is_healthy:
        raise HTTPException(
            status_code=503,
            detail=health_status
        )
        
    return health_status