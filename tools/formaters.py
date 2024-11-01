from datetime import datetime


def date_format(moment):
    return moment.strftime("%Y-%m-%d")


def from_string(selected_date: str):
    return datetime.strptime(selected_date, "%Y-%m-%d")
