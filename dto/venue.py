from dataclasses import dataclass


@dataclass
class Venue:
    name: str = ""
    address: str = ""
    google_maps_url: str = ""
    arrival_parking_info: str = ""
    cloakroom: str = ""
    gastronomy: str = ""
    wheelchair_access: str = ""
    late_admission_info: str = ""