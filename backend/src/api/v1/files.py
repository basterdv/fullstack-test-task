from fastapi import APIRouter, File, Form, UploadFile, Depends,Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.db.config import get_db
from src.db.dao.files import FileDAO
from src.schemas.schemas import FileItem, FileUpdate,PaginatedResponse
from src.services.file_service import FileService
from src.services.storage import FileStorage
from src.tasks import scan_file_for_threats, send_file_alert

router = APIRouter(prefix="/files", tags=["Files"])

@router.get("", response_model=PaginatedResponse[FileItem])
async def list_files_view(
        page: int = Query(1, ge=1),
        size: int = Query(5, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    service = FileService(FileDAO(db))
    items, total = await service.list_active_files(page=page, size=size)

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": (total + size - 1) // size if total > 0 else 0
    }


@router.get("/{file_id}", response_model=FileItem)
async def get_file_view(file_id: str, db: AsyncSession = Depends(get_db), ):
    service = FileService(FileDAO(db))
    return await service.get_file_or_fail(file_id)


@router.post("", response_model=FileItem, status_code=201)
async def create_file_view(
        title: str = Form(...),
        file: UploadFile = File(...),
        action: str = Form(...) ,
        db: AsyncSession = Depends(get_db),
):
    service = FileService(FileDAO(db), FileStorage(settings.STORAGE_DIR))
    file_item = await service.upload_file(
        title=title,
        upload_file=file,
    )

    scan_file_for_threats.delay(file_item.id, action)

    return file_item

@router.get("/{file_id}/download")
async def download_file(
        file_id: str,
        db: AsyncSession = Depends(get_db),
):
    service = FileService(FileDAO(db), FileStorage(settings.STORAGE_DIR))
    action = 'download'
    file_item, stored_path = await service.get_file_for_download(file_id)

    scan_file_for_threats.delay(file_id, action)

    return FileResponse(
        path=stored_path,
        media_type=file_item.mime_type,
        filename=file_item.original_name,
    )

@router.patch("/{file_id}", response_model=FileItem)
async def update_file_view(
        file_id: str,
        payload: FileUpdate,
        db: AsyncSession = Depends(get_db),
):
    service = FileService(FileDAO(db))

    send_file_alert.delay(file_id, payload.action)

    return await service.update_file(file_id=file_id, title=payload.title)


@router.delete("/{file_id}", status_code=204)
async def delete_file_view(
        file_id: str,
        # action: str,
        db: AsyncSession = Depends(get_db),
):
    action = 'delete'

    service = FileService(FileDAO(db), FileStorage(settings.STORAGE_DIR))

    await service.delete_file(file_id)

    send_file_alert.delay(file_id, action)