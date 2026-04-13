from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from src.db.dao.base import BaseDAO
from src.db.models import Alert


class AlertDAO(BaseDAO):

    async def list_alerts(self, limit: int = 10, offset: int = 0) -> tuple[list[Alert], int]:
        count_stmt = select(func.count()).select_from(Alert)
        total_count = await self.session.execute(count_stmt)
        total = total_count.scalar() or 0

        result = await self.session.execute(
            select(Alert)
            .options(joinedload(Alert.file))
            .order_by(Alert.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return list(result.scalars().all()), total


    async def create_alert(self, file_id: str, level: str, message: str) -> Alert:
        alert = Alert(file_id=file_id, level=level, message=message)
        self.session.add(alert)
        return await self.save(alert)
