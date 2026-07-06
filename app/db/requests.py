from app.db.models import User
from app.db.models import async_session
from sqlalchemy import select



async def set_user(
        name: str,
        telegram_id: int
):
    async with async_session() as session:
        user = session.scalar(select(User).where(User.telegram_id == telegram_id))

        if not user:
            session.add(User(name=name, telegram_id=telegram_id))
            await session.commit()


async def get_user_by_telegram_id(
        telegram_id: int
):
    async with async_session() as session:
        res = await session.scalars(select(User).where(User.telegram_id == telegram_id))
        return res.first()

