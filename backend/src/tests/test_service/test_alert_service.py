import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.alert_service import AlertService


@pytest.fixture
def mock_alert_dao():
    dao = MagicMock()
    dao.list_alerts = AsyncMock()
    dao.create_alert = AsyncMock()
    return dao


@pytest.fixture
def alert_service(mock_alert_dao):
    return AlertService(dao=mock_alert_dao)


@pytest.mark.asyncio
class TestAlertService:

    async def test_list_alerts_calls_dao(self, alert_service, mock_alert_dao):
        """Проверка, что сервис вызывает соответствующий метод DAO для списка"""

        mock_alert_dao.list_alerts.return_value = ([{"id": 1, "message": "test"}], 1)

        result = await alert_service.list_alerts()

        # Если сервис возвращает кортеж, проверяем его части
        items, total = result
        assert len(items) == 1
        assert total == 1
        mock_alert_dao.list_alerts.assert_called_once()

    async def test_create_alert_passes_correct_data(self, alert_service, mock_alert_dao):
        """Проверка корректной передачи параметров при создании алерта"""
        file_id = "test-uuid"
        level = "warning"
        message = "Suspicious file detected"

        # Настраиваем мок на возврат
        mock_alert_dao.create_alert.return_value = {
            "file_id": file_id,
            "level": level,
            "message": message
        }

        result = await alert_service.create_alert(file_id, level, message)

        # Проверяем, что DAO был вызван с нужными аргументами
        mock_alert_dao.create_alert.assert_called_once_with(file_id, level, message)
        assert result["level"] == "warning"
