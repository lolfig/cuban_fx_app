from matplotlib import pyplot as plt
import pandas as pd
import uvicorn

from data_storage import data_store  # noqa
from services.framework_scraping.time_series_fetcher import PriceTimeSeries

if __name__ == "__main__":
    # print(data_store.price_series.index)

    print("Iniciando dashboard...")
    uvicorn.run("app:app", host="localhost", port=8000)
