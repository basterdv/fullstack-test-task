import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.db.models import Base, Alert, StoredFile
from src.db.dao.alert import AlertDAO
from datetime import datetime, timedelta, timezone

@pytest.fixture
async def db_session():
    # SQLite  для быстрой локальной проверки DAO
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()

@pytest.mark.asyncio
class TestAlertDAO:

    async def test_create_alert(self, db_session):
        dao = AlertDAO(db_session)
        file_id = "test-file-id"

        test_file = StoredFile(
            id=file_id, title="Test", original_name="t.txt",
            stored_name="s.txt", mime_type="application/octet-stream", size=1024
        )
        db_session.add(test_file)
        await db_session.commit()

        alert = await dao.create_alert(file_id, "warning", "Potential threat")

        assert alert.id is not None
        assert alert.level == "warning"
        assert alert.file_id == file_id

    async def test_list_alerts_with_joined_file(self, db_session):
        dao = AlertDAO(db_session)
        file_id = "file-1"

        test_file = StoredFile(
            id=file_id, title="Main File", original_name="m.txt",
            stored_name="s.txt", mime_type="text/plain", size=500
        )
        db_session.add(test_file)
        await db_session.flush()

        alert = Alert(file_id=file_id, level="info", message="All good")
        db_session.add(alert)
        await db_session.commit()

        alerts, total = await dao.list_alerts()

        assert total == 1
        assert len(alerts) == 1
        assert alerts[0].message == "All good"
        assert alerts[0].file.title == "Main File"

    async def test_list_alerts_sorting(self, db_session):
        dao = AlertDAO(db_session)
        file_id = "file-1"

        now = datetime.now(timezone.utc)

        test_file = StoredFile(
            id=file_id, title="Test", original_name="t.txt",
            stored_name="s.txt", mime_type="text/plain", size=100
        )
        db_session.add(test_file)
        await db_session.flush()

        a1 = Alert(file_id=file_id, level="info", message="First", created_at=now - timedelta(seconds=5))
        a2 = Alert(file_id=file_id, level="error", message="Second", created_at=now)
        db_session.add_all([a1, a2])
        await db_session.commit()


        alerts, total = await dao.list_alerts()

        assert total == 2

        assert alerts[0].message == "Second"
        assert alerts[1].message == "First"
