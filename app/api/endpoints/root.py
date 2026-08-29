from fastapi import APIRouter

from app.models.healthcheck import HealthcheckSchema

router = APIRouter()


@router.get("/health")
def healthcheck() -> HealthcheckSchema:
    return HealthcheckSchema()
