import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from src.tasks import scan_file_for_threats, send_file_alert


class TestCeleryTasks:

    @patch("src.tasks.async_session_maker")
    @patch("src.services.file_service.FileService.service_scan_file_for_threats", new_callable=AsyncMock)
    @patch("src.tasks.extract_file_metadata.delay")
    @patch("src.tasks.run_in_worker_loop")

    def test_scan_file_task_success(self, mock_run_loop, mock_metadata_delay, mock_scan_service, mock_session):
        mock_session.return_value.__aenter__.return_value = AsyncMock()

        def side_effect(coro):
            return asyncio.run(coro)

        mock_run_loop.side_effect = side_effect

        scan_file_for_threats.run("file_123", "upload")

        mock_scan_service.assert_called_once_with("file_123", "upload")
        mock_metadata_delay.assert_called_once()

    @patch("src.tasks.async_session_maker")
    @patch("src.db.dao.files.FileDAO.get_file", new_callable=AsyncMock)
    @patch("src.db.dao.alert.AlertDAO.create_alert", new_callable=AsyncMock)
    @patch("src.tasks.run_in_worker_loop")
    def test_send_file_alert_warning(self, mock_run_loop, mock_create_alert, mock_get_file, mock_session):
        mock_session.return_value.__aenter__.return_value = AsyncMock()

        def side_effect(coro):
            return asyncio.run(coro)

        mock_run_loop.side_effect = side_effect

        fake_file = MagicMock()
        fake_file.requires_attention = True
        fake_file.scan_details = "suspicious"
        fake_file.processing_status = "uploaded"
        mock_get_file.return_value = fake_file

        send_file_alert.run("file_123", "upload")

        mock_create_alert.assert_called_once()
