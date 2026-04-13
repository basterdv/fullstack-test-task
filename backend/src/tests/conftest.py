# import pytest
# from unittest.mock import patch
# from httpx import AsyncClient, ASGITransport
# from backend.src.app import app
#
#
# @pytest.fixture
# async def client():
#     with patch("backend.src.tasks.scan_file_for_threats.delay") as mock_scan, \
#             patch("backend.src.tasks.send_file_alert.delay") as mock_alert, \
#             patch("backend.src.tasks.extract_file_metadata.delay") as mock_meta:
#         async with AsyncClient(
#                 transport=ASGITransport(app=app),
#                 base_url="http://test"
#         ) as ac:
#             yield ac

import os

import pytest
from httpx import AsyncClient, ASGITransport

from backend.src.app import app

# Устанавливаем переменные окружения ДО импорта приложения
os.environ["CELERY_BROKER_URL"] = "memory://"
os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"


@pytest.fixture(autouse=True)
def mock_celery_infra(monkeypatch):
    """
    Автоматически переключает Celery в режим 'eager' (синхронный)
    и подменяет Redis на память для всех тестов.
    """
    from src.tasks import celery_app  # измените путь на ваш импорт celery

    monkeypatch.setattr(celery_app.conf, "task_always_eager", True)
    monkeypatch.setattr(celery_app.conf, "task_eager_propagates", True)
    monkeypatch.setattr(celery_app.conf, "broker_url", "memory://")
    monkeypatch.setattr(celery_app.conf, "result_backend", "cache+memory://")


@pytest.fixture
async def client():
    # Используем ASGITransport — это решает проблему WinError 64
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
