import pytest
from unittest.mock import patch, AsyncMock
from types import SimpleNamespace

def get_mock_file(id="test-uuid", title="My File"):
    return SimpleNamespace(
        id=id,
        title=title,
        original_name="test.txt",
        mime_type="text/plain",
        size=12,
        processing_status="uploaded",
        scan_status="pending",
        scan_details=None,
        requires_attention=False,
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00",
        metadata_json={}
    )


@pytest.mark.asyncio
async def test_create_file(client):
    data = {"title": "My File", "action": "scan"}
    files = {"file": ("test.txt", b"content", "text/plain")}

    with patch("src.services.file_service.FileService.upload_file", new_callable=AsyncMock) as mock_upload, \
            patch("src.api.v1.files.scan_file_for_threats.delay") as mock_scan:
        mock_upload.return_value = get_mock_file()

        response = await client.post("/files", data=data, files=files)

        assert response.status_code == 201
        mock_scan.assert_called_once()


@pytest.mark.asyncio
async def test_update_file(client):
    file_id = "some-uuid"
    payload = {"title": "Updated Title", "action": "update"}

    with patch("src.services.file_service.FileService.update_file", new_callable=AsyncMock) as mock_update, \
            patch("src.api.v1.files.send_file_alert.delay") as mock_alert:
        mock_update.return_value = get_mock_file(id=file_id, title="Updated Title")

        response = await client.patch(f"/files/{file_id}", json=payload)

        assert response.status_code == 200
        assert response.json()["title"] == "Updated Title"
        mock_alert.assert_called_once()
