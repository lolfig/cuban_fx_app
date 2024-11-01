import pandas as pd

from tools.const import DIR_DATA_MESSAGES


def load_data(path):
    print("loading files")
    try:
        analytics = pd.read_pickle(f'{path}/analytics.pickle')
        serie = pd.read_pickle(f'{path}/USDCUP.pickle')
        return analytics, serie
    except FileNotFoundError:
        return None


def load_time_series(analytics, series):
    price_series = series.assign(
        USDCUP_Marginal=analytics['Marginal_Data'].apply(lambda x: x[0]['price_mar'] if x else None)
    )
    price_series.index = price_series.index.date

    volumes_series = analytics[['Volumen_Compra', 'Volumen_Venta', 'Volumen_Total']].assign(
        Volumen_Marginal=analytics['Marginal_Data'].apply(lambda x: x[0]['vol_mar'] if x else None)
    )
    volumes_series.index = volumes_series.index.date

    return price_series, volumes_series


def get_messages_metrics(analytics):
    avg_daily_messages = round(
        (sum(
            [len(i) for i in analytics['Cantidad_Compra']]
        ) + sum(
            [len(i) for i in analytics['Cantidad_Venta']]
        )) / len(analytics)
    )
    messages_compra = sum([len(i) for i in analytics['Cantidad_Compra']])
    messages_venta = sum([len(i) for i in analytics['Cantidad_Venta']])
    percent_compra = round(messages_compra / (messages_compra + messages_venta), 2) * 100
    percent_venta = round(messages_venta / (messages_compra + messages_venta), 2) * 100

    return avg_daily_messages, messages_compra, messages_venta, percent_compra, percent_venta


def get_time_serie_num_messages(analytics):
    return pd.DataFrame(
        {
            'Mensajes_Compra': [len(i) for i in analytics['Cantidad_Compra']],
            'Mensajes_Venta': [len(i) for i in analytics['Cantidad_Venta']]
        }, index=analytics.index
    )


def prepare_daily_data(analytics):
    daily_data = {}
    for date in analytics.index.unique():
        daily_data[date] = {
            'Compras_ordenadas': analytics.loc[date]['Compras_ordenadas'],
            'Ventas_ordenadas': analytics.loc[date]['Ventas_ordenadas'],
            'Nivel_volumen_compra': analytics.loc[date]['Nivel_volumen_compra'],
            'Nivel_precio_compra': analytics.loc[date]['Nivel_precio_compra'],
            'Nivel_volumen_venta': analytics.loc[date]['Nivel_volumen_venta'],
            'Nivel_precio_venta': analytics.loc[date]['Nivel_precio_venta']
        }
    return daily_data


def load_raw_messages(date):
    try:
        mess = pd.read_parquet(f"{DIR_DATA_MESSAGES}/{date}.parquet")
        return mess.iloc[:, :2]
    except FileNotFoundError:
        return pd.DataFrame()
