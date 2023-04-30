import json
from dataclasses import dataclass


@dataclass
class DailyRate:
    date: str
    rates: dict

    def to_dict(self) -> dict:
        return {"date": self.date, "rates": self.rates}

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "DailyRate":
        return cls(date=item["date"], rates=json.loads(item["rates"]))
