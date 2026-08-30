from fastapi import APIRouter

from app.models.healthcheck import HealthcheckView

router = APIRouter()


@router.get("/health")
def healthcheck() -> HealthcheckView:
    return HealthcheckView()
