from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, obj=None):
        """Сохраняет изменения в базе. Если передан obj, делает refresh."""
        await self.session.commit()
        if obj:
            await self.session.refresh(obj)
        return obj
