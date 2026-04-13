from sqlalchemy import select, func
from src.db.dao.base import BaseDAO
from src.db.models import StoredFile


class FileDAO(BaseDAO):
    async def list_files(self, limit: int =10, offset: int = 0) -> tuple[list[StoredFile],int]:
        stmt = select(StoredFile).where(StoredFile.is_deleted == False)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_count = await self.session.execute(count_stmt)
        total = total_count.scalar() or 0

        result = await self.session.execute(
            stmt.order_by(StoredFile.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        return list(result.scalars().all()), total

    async def get_file(self, file_id: str) -> StoredFile | None:
        return await self.session.get(StoredFile, file_id)

    async def create_file(self, file_item: StoredFile) -> StoredFile:
        self.session.add(file_item)
        return await self.save(file_item)

