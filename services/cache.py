import pandas as pd
import emd
from hmmlearn import hmm

from config.const import DIR_DATA_MESSAGES
from services.framework_scraping.time_series_fetcher import PriceTimeSeries


def load_data(path):
    try:
        analytics = pd.read_pickle(f"{path}/analytics.pickle")
        serie = PriceTimeSeries.load_from_file(path, "USD")
        return analytics, serie
    except FileNotFoundError as e:
        print("No se encontraron los ficheros")
        raise e


def generate_time_series(analytics, series):
    print("aqui")
    marginal_price = analytics["Marginal_Data"].apply(
        lambda x: x[0]["price_mar"] if x else None
    )
    marginal_price.index = pd.to_datetime(marginal_price.index)
    price_series = series.assign(USDCUP_Marginal=marginal_price)
    price_series.index = price_series.index.date

    volumes_series = analytics[
        ["Volumen_Compra", "Volumen_Venta", "Volumen_Total"]
    ].assign(
        Volumen_Marginal=analytics["Marginal_Data"].apply(
            lambda x: x[0]["vol_mar"] if x else None
        )
    )
    volumes_series.sort_index(inplace=True)
    # volumes_series.index = volumes_series.index.date

    return price_series, volumes_series


def get_messages_metrics(analytics):
    avg_daily_messages = round(
        (
            sum([len(i) for i in analytics["Cantidad_Compra"]])
            + sum([len(i) for i in analytics["Cantidad_Venta"]])
        )
        / len(analytics)
    )
    messages_compra = sum([len(i) for i in analytics["Cantidad_Compra"]])
    messages_venta = sum([len(i) for i in analytics["Cantidad_Venta"]])
    percent_compra = (
        round(messages_compra / (messages_compra + messages_venta), 2) * 100
    )
    percent_venta = round(messages_venta / (messages_compra + messages_venta), 2) * 100

    return (
        avg_daily_messages,
        messages_compra,
        messages_venta,
        percent_compra,
        percent_venta,
    )


def get_time_serie_num_messages(analytics):
    analytics.sort_index(inplace=True)
    return pd.DataFrame(
        {
            "Mensajes_Compra": [len(i) for i in analytics["Cantidad_Compra"]],
            "Mensajes_Venta": [len(i) for i in analytics["Cantidad_Venta"]],
        },
        index=analytics.index.sort_values(),
    )


def prepare_daily_data(analytics):
    daily_data = {}
    for date in analytics.index.unique():
        daily_data[date] = {
            "Compras_ordenadas": analytics.loc[date]["Compras_ordenadas"],
            "Ventas_ordenadas": analytics.loc[date]["Ventas_ordenadas"],
            "Nivel_volumen_compra": analytics.loc[date]["Nivel_volumen_compra"],
            "Nivel_precio_compra": analytics.loc[date]["Nivel_precio_compra"],
            "Nivel_volumen_venta": analytics.loc[date]["Nivel_volumen_venta"],
            "Nivel_precio_venta": analytics.loc[date]["Nivel_precio_venta"],
        }
    return daily_data


def load_raw_messages(date):
    try:
        mess = pd.read_parquet(f"{DIR_DATA_MESSAGES}/{date}.parquet")
        return mess.iloc[:, :2]
    except FileNotFoundError:
        return pd.DataFrame()


def get_imfs(price_series):
    col = price_series.columns[2]
    serie = price_series[col].values
    imf = emd.sift.sift(serie)
    nIMFs = imf.shape[1]

    return imf.T


def hidden_MM(all_info, num_states, n_iter):

    # time = price_series.index
    # serie = price_series[["USDCUP_Marginal"]]
    # currency = "USD/CUP"

    data_frame = pd.DataFrame(
        {
            "Time": pd.to_datetime(all_info["_id"]),
            "Currency": all_info["avg"],
            "Returns": all_info["avg"].diff(),
        }
    )
    data_frame.dropna(inplace=True)
    returns = data_frame[["Returns"]].values

    model = hmm.GaussianHMM(
        n_components=num_states,
        covariance_type="full",
        n_iter=n_iter,
        random_state=42,
        algorithm="map",
    )
    model.fit(returns)

    Z = model.predict(returns)

    states = pd.unique(Z)

    data_frame["States"] = Z

    # print("Unique states:")
    # print(states)
    # print("\nStart probabilities:")
    # print(model.startprob_)
    # print("\nTransition matrix:")
    # print(model.transmat_)
    # print("\nGaussian distribution means:")
    # print(model.means_)
    # print("\nGaussian distribution covariances:")
    # print(model.covars_)

    data_frame.reset_index(inplace=True)
    del data_frame["index"]

    return data_frame
