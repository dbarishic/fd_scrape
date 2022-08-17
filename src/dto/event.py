from dataclasses import dataclass
from datetime import date
from datetime import datetime
from datetime import time
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .common_base import Base
from .event_performer import event_performer
from .performer import Performer


@dataclass
class Event(Base):
    __tablename__ = "event"

    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: str = Column(String())
    image_url: str = Column(String())
    e_date: date = Column(Date())
    e_time: time = Column(Time())
    description: str = Column(Text())
    program: str = Column(Text())
    festival: str = Column(Text())
    price: int = Column(Numeric(15, 2))
    ticket_purchase_url: str = Column(String())
    performers: list[Performer] = relationship(
        "Performer", secondary=event_performer, lazy="selectin"
    )

    venue_id: str = Column("venue_id", UUID(as_uuid=True), ForeignKey("venue.venue_id"))
    venue = relationship("Venue", back_populates="events", lazy="selectin")

    performer_id: str = Column(
        "performer_id", UUID(as_uuid=True), ForeignKey("performer.performer_id")
    )
    performer = relationship("Performer", back_populates="events", lazy="selectin")

    def __post_init__(self):
        self.e_time = datetime.strptime(f"{str(self.e_time)}.00", "%H.%M.%S").time()
        self.e_time = datetime.time()
