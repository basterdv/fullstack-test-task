from fastapi import APIRouter
from src.api.v1.files import router as files_router
from src.api.v1.alerts import router as alerts_router

api_router = APIRouter(prefix="")
api_router.include_router(files_router)
api_router.include_router(alerts_router)
