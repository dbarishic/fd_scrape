from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .common_base import Base
from .event_performer import event_performer


@dataclass
class Performer(Base):
    __tablename__ = "performer"

    performer_id: str = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    p_name: str = Column(String())
    description: str = Column(Text())
    events: list = relationship(
        "Event", secondary=event_performer, back_populates="performers", lazy="selectin"
    )
