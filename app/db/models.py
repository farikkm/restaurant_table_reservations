from sqlalchemy import String, Integer, Boolean, ForeignKey, Date, Time, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
async_session = async_sessionmaker(engine)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Table(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer)
    capacity: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))

    date: Mapped[Date] = mapped_column(Date)
    time: Mapped[Time] = mapped_column(Time)
    guests: Mapped[int] = mapped_column(Integer)

    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    table = relationship("Table")
    user = relationship("User")


async def start_running():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)