import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import UploadFile, HTTPException
from pathlib import Path
from src.services.file_service import FileService


@pytest.fixture
def mock_dao():
    dao = MagicMock()
    dao.get_file = AsyncMock()
    dao.create_file = AsyncMock()
    dao.save = AsyncMock()
    dao.list_files = AsyncMock()
    return dao


@pytest.fixture
def mock_storage():
    storage = MagicMock()
    storage.save = MagicMock()
    storage.delete = MagicMock()
    storage.get_full_path = MagicMock()
    return storage


@pytest.fixture
def file_service(mock_dao, mock_storage):
    return FileService(dao=mock_dao, storage=mock_storage)


@pytest.mark.asyncio
class TestFileService:

    async def test_upload_file_empty_content(self, file_service):
        """Проверка ошибки при загрузке пустого файла"""
        mock_upload = AsyncMock(spec=UploadFile)
        mock_upload.read.return_value = b""

        with pytest.raises(HTTPException) as exc:
            await file_service.upload_file("Title", mock_upload)

        assert exc.value.status_code == 400
        assert "empty" in exc.value.detail

    async def test_upload_file_success(self, file_service, mock_dao, mock_storage):
        """Проверка успешной загрузки и вызова сохранения"""
        mock_upload = AsyncMock(spec=UploadFile)
        mock_upload.read.return_value = b"hello world"
        mock_upload.filename = "test.txt"
        mock_upload.content_type = "text/plain"

        # Настраиваем DAO, чтобы он возвращал то, что получил
        mock_dao.create_file.side_effect = lambda x: x

        result = await file_service.upload_file("My File", mock_upload)

        assert result.title == "My File"
        assert result.size == 11
        mock_storage.save.assert_called_once()  # Проверяем, что файл записан в хранилище
        mock_dao.create_file.assert_called_once()  # Проверяем запись в БД

    async def test_scan_file_suspicious_extension(self, file_service, mock_dao):
        """Проверка детекции подозрительного расширения (.exe)"""
        # Создаем мок объекта файла
        file_item = MagicMock()
        file_item.original_name = "virus.exe"
        file_item.size = 100
        file_item.is_deleted = False

        mock_dao.get_file.return_value = file_item

        await file_service.service_scan_file_for_threats("uuid", "scan")

        assert file_item.scan_status == "suspicious"
        assert "suspicious extension .exe" in file_item.scan_details
        assert file_item.requires_attention is True

    async def test_get_file_for_download_not_exists_in_storage(self, file_service, mock_dao, mock_storage):
        """Ошибка, если запись в БД есть, а файла на диске нет"""
        file_item = MagicMock(is_deleted=False, stored_name="file.txt")
        mock_dao.get_file.return_value = file_item

        # Мокаем путь, который "не существует"
        mock_path = MagicMock(spec=Path)
        mock_path.exists.return_value = False
        mock_storage.get_full_path.return_value = mock_path

        with pytest.raises(HTTPException) as exc:
            await file_service.get_file_for_download("uuid")

        assert exc.value.status_code == 404
        assert "missing on storage" in exc.value.detail

    async def test_delete_file_already_deleted(self, file_service, mock_dao, mock_storage):
        """Если файл уже удален, повторного удаления не происходит"""
        file_item = MagicMock(is_deleted=True)
        mock_dao.get_file.return_value = file_item

        await file_service.delete_file("uuid")

        mock_storage.delete.assert_not_called()
        mock_dao.save.assert_not_called()
