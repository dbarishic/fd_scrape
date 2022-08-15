from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Price:
    value: Decimal
    currency: str