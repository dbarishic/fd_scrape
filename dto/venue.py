from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Venue:
    venue_id = uuid4()
    name: str = ""
    address: str = ""
    google_maps_url: str = ""
    arrival_parking_info: str = ""
    cloakroom: str = ""
    gastronomy: str = ""
    wheelchair_access: str = ""
    late_admission_info: str = ""