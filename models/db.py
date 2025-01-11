from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (Mapped, declarative_base, declared_attr,
                            mapped_column, sessionmaker)

from config import config


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(str(config['DB']['url']))

Session = sessionmaker(engine, class_=AsyncSession)
