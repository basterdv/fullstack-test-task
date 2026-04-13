import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.db.models import Base, StoredFile
from src.db.dao.files import FileDAO


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
class TestFileDAO:
    async def test_create_and_get_file(self, db_session):
        dao = FileDAO(db_session)
        file_obj = StoredFile(
            id="test-id", title="Test File", original_name="test.txt",
            stored_name="test_stored.txt", mime_type="application/octet-stream", size=100
        )
        created_file = await dao.create_file(file_obj)
        assert created_file.id == "test-id"

        fetched_file = await dao.get_file("test-id")
        assert fetched_file.title == "Test File"

    async def test_list_files_filters_deleted(self, db_session):
        dao = FileDAO(db_session)

        f1 = StoredFile(id="1", title="A", is_deleted=False, original_name="1.txt",
                        stored_name="1s.txt", mime_type="text/plain", size=10)
        f2 = StoredFile(id="2", title="B", is_deleted=True, original_name="2.txt",
                        stored_name="2s.txt", mime_type="text/plain", size=10)
        db_session.add_all([f1, f2])
        await db_session.commit()

        files, total = await dao.list_files()
        assert len(files) == 1
        assert total == 1
        assert files[0].id == "1"

    async def test_list_files_sorting(self, db_session):
        dao = FileDAO(db_session)
        now = datetime.now(timezone.utc)

        f1 = StoredFile(id="old", title="Old", created_at=now - timedelta(minutes=5),
                        original_name="o.txt", stored_name="os.txt", mime_type="t", size=1)
        f2 = StoredFile(id="new", title="New", created_at=now,
                        original_name="n.txt", stored_name="ns.txt", mime_type="t", size=1)

        db_session.add_all([f1, f2])
        await db_session.commit()

        files, total = await dao.list_files()

        assert files[0].id == "new"
        assert files[1].id == "old"

    async def test_get_non_existent_file(self, db_session):
        dao = FileDAO(db_session)
        assert await dao.get_file("unknown") is None
