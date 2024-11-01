# tools
from tools.const import DIR_DATA_ANALYTICS, DIR_DATA_MESSAGES
from framework_scraping.tools.missing_dates import get_missing_dates
# framework
from framework_scraping.definitions import DataProcessing, PriceTimeSeries
from framework_analytics.definitions import DataAnalytics


def main():
    missing_dates = get_missing_dates(DIR_DATA_MESSAGES)

    if len(missing_dates.dates) > 0:
        print(f"Missing dates found: {','.join(missing_dates.dates)}")

        fetcher = DataProcessing(end_dates=missing_dates.dates, currency="USD")
        fetcher.do_process_messages()

        analytics = DataAnalytics(DIR_DATA_MESSAGES)
        analytics.do_analytics()
        analytics.dataframe.to_pickle(f"{DIR_DATA_ANALYTICS}/analytics.pickle")

        price_series = PriceTimeSeries(
            missing_dates.start_date, missing_dates.end_date, DIR_DATA_ANALYTICS, ['Compra', 'Venta'], currency='USD'
        )
        price_series.get_time_series()

    print("Iniciando dashboard...")

    from app_dashboard.dashboard_app import app
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
