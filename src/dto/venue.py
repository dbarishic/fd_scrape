from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy.orm import relationship

from common_base import Base
from .event import Event


@dataclass
class Venue(Base):
    __tablename__ = "venue"

    venue_id = uuid4()
    name: str = ""
    address: str = ""
    google_maps_url: str = ""
    arrival_parking_info: str = ""
    cloakroom: str = ""
    gastronomy: str = ""
    wheelchair_access: str = ""
    late_admission_info: str = ""
    events: list[Event] = relationship("Event", back_populates="venue", lazy="selectin")
