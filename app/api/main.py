import logging

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.api.endpoints.readers import router as reader_router
from app.api.endpoints.root import router as root_router
from app.api.exception_handlers import register_exception_handlers
from app.core.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
add_pagination(app)
register_exception_handlers(app)


v1_router = APIRouter(prefix="/api/v1")


# TODO: Include routers
v1_router.include_router(root_router)
v1_router.include_router(reader_router, prefix="/readers", tags=["readers"])


app.include_router(v1_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)