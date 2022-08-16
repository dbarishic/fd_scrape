from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Performer:
    performer_id = uuid4()
    name: str
    description: str
