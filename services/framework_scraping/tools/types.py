from dataclasses import dataclass
from typing import List, Any, Tuple


@dataclass
class MessagesStep:
  end: str
  start: str
  messages: List[Any]


@dataclass
class DateExistenceReport:
  start_date: str
  end_date: str
  
  # all_data_days
  dates: List[
    Tuple[
      str  # date
      , bool  # is in list
    ]
  ]
