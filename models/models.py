from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from models.db import Base


class User(Base):
    chat_id: Mapped[int]

    locations: Mapped[List["Location"]] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


class Location(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    latitude: Mapped[float]
    longitude: Mapped[float]
    name: Mapped[str]

    user: Mapped["User"] = relationship(back_populates='locations')
    subscriptions: Mapped[List["Subscription"]] = relationship(
        back_populates='location', cascade='all, delete-orphan'
    )


class Subscription(Base):
    location_id: Mapped[int] = mapped_column(ForeignKey('location.id'))
    detail_type: Mapped[str] # detailed / short i know it could be an enum
    next_event_time: Mapped[datetime] = mapped_column(insert_default=func.now())
    period: Mapped[int] # the number of hours in between the sends

    location: Mapped["Location"] = relationship(back_populates='subscriptions')
