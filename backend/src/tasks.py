import asyncio

from celery import Celery

from src.core.config import settings
from src.db.config import async_session_maker
from src.db.dao.alert import AlertDAO
from src.db.dao.files import FileDAO
from src.services.file_service import FileService
from src.services.storage import FileStorage

_worker_loop: asyncio.AbstractEventLoop | None = None

def run_in_worker_loop(coroutine):
    global _worker_loop
    if _worker_loop is None or _worker_loop.is_closed():
        _worker_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_worker_loop)
    return _worker_loop.run_until_complete(coroutine)

celery_app = Celery("file_tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery_app.task(name="scan_file_for_threats")
def scan_file_for_threats(file_id: str, action: str):
    async def _run():
        async with async_session_maker() as session:
            service = FileService(FileDAO(session), FileStorage(settings.STORAGE_DIR))
            await service.service_scan_file_for_threats(file_id, action)

            extract_file_metadata.delay(file_id,action)

    run_in_worker_loop(_run())


@celery_app.task(name="extract_file_metadata")
def extract_file_metadata(file_id: str,action: str):
    async def _run():
        async with async_session_maker() as session:
            service = FileService(FileDAO(session), FileStorage(settings.STORAGE_DIR))
            await service.service_extract_file_metadata(file_id,action)
            send_file_alert.delay(file_id,action)

    run_in_worker_loop(_run())


@celery_app.task(name="send_file_alert")
def send_file_alert(file_id: str,action: str):
    async def _run():
        async with async_session_maker() as session:
            file_dao = FileDAO(session)
            alert_dao = AlertDAO(session)

            file = await file_dao.get_file(file_id)
            if not file:
                return

            msg = f"File {action} processed successfully"
            level = "info"
            if file.processing_status == "failed":
                msg, level = "File processing failed", "critical"
            elif file.requires_attention and action == 'upload':
                msg, level = f"File requires attention: {file.scan_details}", "warning"

            await alert_dao.create_alert(file_id, level, msg)

    run_in_worker_loop(_run())
