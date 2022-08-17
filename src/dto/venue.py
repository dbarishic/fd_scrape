from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .common_base import Base
from .event import Event


@dataclass
class Venue(Base):
    __tablename__ = "venue"

    venue_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    v_name: str = Column(String())
    address: str = Column(String())
    google_maps_url: str = Column(String())
    arrival_parking_info: str = Column(Text())
    cloakroom: str = Column(Text())
    gastronomy: str = Column(Text())
    wheelchair_access: str = Column(Text())
    late_admission_info: str = Column(Text())
    events: list[Event] = relationship("Event", back_populates="venue", lazy="selectin")
