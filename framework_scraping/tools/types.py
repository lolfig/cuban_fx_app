from dataclasses import dataclass
from typing import List, Any


@dataclass
class MessagesStep:
    end: str
    start: str
    messages: List[Any]


@dataclass
class MissingDates:
    start_date: str
    end_date: str
    dates: List[str]
