from enum import Enum


class Airport(Enum):
    """Enum for various airports."""
    MAD = ("MAD", "Madrid")
    RTM = ("RTM", "Rotterdam")
    SOF = ("SOF", "Sofia")
    
    def __init__(self, code, city):
        self.code = code
        self.city = city

    @classmethod
    def from_string(cls, value: str):
        """Get Airport enum member from string code or city name."""
        for member in cls:
            if member.code.lower() == value.lower() or member.city.lower() == value.lower():
                return member
        raise ValueError(f"Unknown airport: {value}")
    

class TravelDirection(Enum):
    """Enum for travel direction types."""
    ONE_WAY = ("oneWay", "one-way")
    RETURN = ("return")
    MULICITY = ("multicity")
    NOMAD = ("nomad")

    def __init__(self, page_code, alias: str = None):
        self.page_code = page_code
        self.alias = alias

    @classmethod
    def from_string(cls, value: str):
        """Get TravelDirection enum member from string page code or alias."""
        for member in cls:
            if (member.page_code.lower() == value.lower() or 
                (member.alias and member.alias.lower() == value.lower())):
                return member
        raise ValueError(f"Unknown travel direction: {value}")        

