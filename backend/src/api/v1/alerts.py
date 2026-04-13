from src.schemas.schemas import AlertItem,PaginatedResponse
from src.services.alert_service import AlertService
from src.db.dao.alert import AlertDAO
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends,Query
from src.db.config import get_db
router = APIRouter(prefix="/alerts", tags=["Alerts"])
@router.get("", response_model=PaginatedResponse[AlertItem])
async def list_alerts_view(
        page: int = Query(1, ge=1),
        size: int = Query(5, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    service = AlertService(AlertDAO(db))
    items, total = await service.list_alerts(page=page, limit=size)

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size
    }

@router.post("/{file_id}/alerts", response_model=AlertItem)
async def add_alert(
        file_id: str,
        level: str,
        message: str,
        db: AsyncSession = Depends(get_db)
):
    service = AlertService(AlertDAO(db))
    return await service.create_alert(file_id, level, message)
