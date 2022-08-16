from dataclasses import dataclass, field
from datetime import date, time

from sqlalchemy import Column, Text, Numeric, String, Date, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .performer import Performer
from .venue import Venue
from common_base import Base

@dataclass
class Event(Base):
    __tablename__ = "event"

    event_id = Column(UUID)
    title: str = Column(String(250))
    image_url = str = Column(String(250))
    date: date = Column(Date())
    time: time = Column(Time())
    description: str = Column(Text())
    program: str = Column(Text())
    festival: str = Column(Text())
    price: int = Column(Numeric(15, 2))
    ticket_purchase_url: str = Column(String(250))
    performers: list[Performer] = field(default_factory=list)

    venue_id: str = Column("venue_id", UUID(), ForeignKey("Venue.venue_id"))
    venue = relationship(Venue, back_populates="events")