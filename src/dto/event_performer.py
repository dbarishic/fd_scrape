from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table

from .common_base import Base

event_performer = Table(
    "event_performer",
    Base.metadata,
    Column("event_id", ForeignKey("event.event_id"), primary_key=True),
    Column("performer_id", ForeignKey("performer.performer_id"), primary_key=True),
)
