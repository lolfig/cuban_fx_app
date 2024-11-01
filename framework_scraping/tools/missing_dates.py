import datetime
import os

import pandas as pd

from tools.const import DIR_DATA_MESSAGES
from framework_scraping.tools.types import MissingDates


def get_missing_dates(data_dir: str) -> MissingDates:
    start_date = datetime.datetime.strptime("2022-08-01", "%Y-%m-%d")
    end_date = datetime.datetime.now() - datetime.timedelta(days=1)

    all_dates = [
        (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((end_date - start_date).days + 1)
    ]

    existing_files = os.listdir(data_dir)
    existing_dates = [file.split('.')[0] for file in existing_files if file.endswith('.parquet')]

    missing_dates = [date for date in all_dates if date not in existing_dates]

    return MissingDates(
        dates=missing_dates,
        start_date=all_dates[0],
        end_date=all_dates[-1]
    )


def load_messages(date) -> None:
    filename = f"{date}.parquet"
    file_path = os.path.join(DIR_DATA_MESSAGES, filename)
    df = pd.read_parquet(file_path)
    return df
