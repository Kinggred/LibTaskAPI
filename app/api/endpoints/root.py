from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def healthcheck():
    # TODO: DB Check maybe
    return {"status": "ok"}
