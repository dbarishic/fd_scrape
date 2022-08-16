from dataclasses import dataclass, field
from datetime import date, time
from uuid import uuid4

from dto.performer import Performer
from dto.price import Price
from dto.venue import Venue


@dataclass
class Event:
    event_id = uuid4()
    title: str = ""
    image_url = str = ""
    venue: Venue = None
    date: date = None
    time: time = None
    description: str = ""
    program: str = ""
    festival: str = ""
    price: Price = None
    ticket_purchase_url: str = ""
    performers: list[Performer] = field(default_factory=list)
