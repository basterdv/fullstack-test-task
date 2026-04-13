from src.db.dao.alert import AlertDAO


class AlertService:
    def __init__(self, dao: AlertDAO):
        self.dao = dao

    async def list_alerts(self, page: int = 1, limit: int = 10):
        offset = (page - 1) * limit
        items, total = await self.dao.list_alerts(limit = limit, offset = offset)
        return items, total


    async def create_alert(self, file_id: str, level: str, message: str):
        # TODO можно добавить валидацию уровня (info/error/warning)
        return await self.dao.create_alert(file_id, level, message)


