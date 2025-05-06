from matplotlib import pyplot as plt
import pandas as pd
import uvicorn

from data_storage import data_store  # noqa
from services.framework_scraping.time_series_fetcher import PriceTimeSeries

if __name__ == "__main__":
    print("Iniciando dashboard...")
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
