from fastapi import UploadFile, HTTPException, status
from src.db.models import StoredFile
from src.services.storage import FileStorage
from src.db.dao.files import FileDAO
from uuid import uuid4
from pathlib import Path


class FileService:
    def __init__(self, dao: FileDAO, storage: FileStorage | None = None):
        self.dao = dao
        self.storage = storage

    async def list_active_files(self, page: int = 1, size: int = 10) -> tuple[list[StoredFile], int]:
        offset = (page - 1) * size
        return await self.dao.list_files(limit=size, offset=offset)

    async def upload_file(self, title: str, upload_file: UploadFile) -> StoredFile:
        content = await upload_file.read()
        if not content:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "File is empty")

        file_id = str(uuid4())
        suffix = Path(upload_file.filename or "").suffix
        stored_name = f"{file_id}{suffix}"

        self.storage.save(stored_name, content)

        file_item = StoredFile(
            id=file_id,
            title=title,
            original_name=upload_file.filename or stored_name,
            stored_name=stored_name,
            mime_type=upload_file.content_type or "application/octet-stream",
            size=len(content),
            processing_status="uploaded"
        )
        return await self.dao.create_file(file_item)

    async def delete_file(self, file_id: str) -> None:
        file_item = await self.dao.get_file(file_id)

        if not file_item:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")

        if file_item.is_deleted:
            return

        if self.storage:
            self.storage.delete(file_item.stored_name)

        file_item.is_deleted = True
        file_item.processing_status = "deleted"
        await self.dao.save()

    async def update_file(self, file_id: str, title: str) -> StoredFile:

        file_item = await self.get_file_or_fail(file_id)

        file_item.title = title

        return await self.dao.save(file_item)

    async def get_file_or_fail(self, file_id: str) -> StoredFile:
        file_item = await self.dao.get_file(file_id)
        if not file_item or file_item.is_deleted:
            raise HTTPException(status_code=404, detail="File not found")
        return file_item

    async def get_file_for_download(self, file_id: str) -> tuple[StoredFile, Path]:

        file_item = await self.get_file_or_fail(file_id)

        stored_path = self.storage.get_full_path(file_item.stored_name)

        if not stored_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File content missing on storage"
            )

        return file_item, stored_path

    async def service_scan_file_for_threats(self, file_id: str, action: str) -> None:
        file_item = await self.get_file_or_fail(file_id)
        file_item.processing_status = "processing"

        reasons: list[str] = []
        extension = Path(file_item.original_name).suffix.lower()

        if extension in {".exe", ".bat", ".cmd", ".sh", ".js"}:
            reasons.append(f"suspicious extension {extension}")

        if file_item.size > 10 * 1024 * 1024:
            reasons.append("file is larger than 10 MB")

        if extension == ".pdf" and file_item.mime_type not in {"application/pdf", "application/octet-stream"}:
            reasons.append("pdf extension does not match mime type")

        file_item.scan_status = "suspicious" if reasons else "clean"
        file_item.scan_details = ", ".join(reasons) if reasons else "no threats found"
        file_item.requires_attention = bool(reasons)
        return await self.dao.save(file_item)

    async def service_extract_file_metadata(self, file_id: str, action: str) -> bool:
        file_item = await self.get_file_or_fail(file_id)
        path = self.storage.get_full_path(file_item.stored_name)

        if not path.exists():
            file_item.processing_status = "failed"
            file_item.scan_status = file_item.scan_status or "failed"
            file_item.scan_details = "stored file not found during metadata extraction"
            await self.dao.save(file_item)
            return False

        metadata = {
            "extension": Path(file_item.original_name).suffix.lower(),
            "size_bytes": file_item.size,
            "mime_type": file_item.mime_type,
        }
        try:
            if file_item.mime_type.startswith("text/"):
                content = path.read_text(encoding="utf-8", errors="ignore")
                metadata["line_count"] = len(content.splitlines())
                metadata["char_count"] = len(content)
            elif file_item.mime_type == "application/pdf":
                content = path.read_bytes()
                metadata["approx_page_count"] = max(content.count(b"/Type /Page"), 1)

            file_item.metadata_json = metadata
            file_item.processing_status = "processed"
            await self.dao.save(file_item)
            return True
        except Exception as e:
            file_item.processing_status = "failed"
            file_item.scan_details = f"Metadata extraction error: {str(e)}"
            await self.dao.save(file_item)
            return False
