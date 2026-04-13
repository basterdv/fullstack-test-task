from datetime import datetime,timezone
import pytest
from unittest.mock import patch
from unittest.mock import AsyncMock
@pytest.mark.asyncio
async def test_create_alert_success(client):
    file_id = "test-uuid-123"
    expected_response = {
        "id": 1,
        "file_id": file_id,
        "level": "warning",
        "message": "Potential threat detected",
        "created_at": datetime.now(timezone.utc)
    }

    with patch("backend.src.api.v1.alerts.AlertService.create_alert", new_callable=AsyncMock) as mock_create:
        mock_create.return_value = expected_response

        response = await client.post(
            f"/alerts/{file_id}/alerts",
            params={"level": "warning", "message": "Potential threat detected"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
