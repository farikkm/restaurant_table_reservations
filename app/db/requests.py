from sqlalchemy import select

from app.db.models import async_session, Reservation


async def create_reservation(user_id: int, table_id: int, date, time, guests: int):
    async with async_session() as session:
        reservation = Reservation(
            user_id=user_id,
            table_id=table_id,
            date=date,
            time=time,
            guests=guests,
            status="active"
        )

        session.add(reservation)
        await session.commit()
        await session.refresh(reservation)

        return reservation


async def get_user_reservations(user_id: int):
    async with async_session() as session:
        reservations = await session.scalars(
            select(Reservation).where(Reservation.user_id == user_id)
        )

        return reservations.all()


async def delete_reservation(reservation_id: int):
    async with async_session() as session:
        reservation = await session.scalar(
            select(Reservation).where(Reservation.id == reservation_id)
        )

        if reservation:
            await session.delete(reservation)
            await session.commit()
            return True

        return False