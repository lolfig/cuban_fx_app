from datetime import datetime, date


def from_string(selected_date: str):
  return datetime.strptime(selected_date, "%Y-%m-%d")


def datetime_to_str(date_instance) -> str:
  if isinstance(date_instance, (datetime, date)):
    return date_instance.strftime("%Y-%m-%d")
  return date_instance
