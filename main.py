import json
import dash
import dash_bootstrap_components as dbc

# tools
from tools.const import DIR_DATA_ANALYTICS, DIR_DATA_MESSAGES

# framework
from framework_scraping.tools.missing_dates import get_missing_dates
from framework_scraping.definitions import DataProcessing, PriceTimeSeries
from framework_analytics.definitions import DataAnalytics


def main():
    missing_dates = get_missing_dates(DIR_DATA_MESSAGES)

    # if len(missing_dates.dates) > 0:
    #     print(f"Missing dates found: {','.join(missing_dates.dates)}")

    #     fetcher = DataProcessing(end_dates=missing_dates.dates, currency="USD")
    #     fetcher.do_process_messages()

    analytics = DataAnalytics(DIR_DATA_MESSAGES)
    analytics.do_analytics()
    analytics.dataframe.to_pickle(f"{DIR_DATA_ANALYTICS}/analytics.pickle")

    with open(f"{DIR_DATA_ANALYTICS}/all_orders.json", "w") as file:
        json.dump(analytics.orders, file)

    price_series = PriceTimeSeries(
        missing_dates.start_date,
        missing_dates.end_date,
        DIR_DATA_ANALYTICS,
        ["Compra", "Venta"],
        currency="USD",
    )
    price_series.get_time_series()

    print("Iniciando dashboard...")

    from app_dashboard import load_dashboard

    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP
        ]
    )
    load_dashboard(app)

    app.run_server(debug=True)


if __name__ == "__main__":
    main()
