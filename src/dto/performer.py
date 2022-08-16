from dataclasses import dataclass
from uuid import uuid4

from common_base import Base


@dataclass
class Performer(Base):
    __tablename__ = "performer"

    performer_id = uuid4()
    name: str
    description: str
