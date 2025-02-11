import calendar
from itertools import chain

import dash_bootstrap_components as dbc
import pandas as pd

from app import data_store
from components import head_lines as custom_head_lines
from components.tables import create_table


def generate_git_hub_days_counter_content():
  df = pd.DataFrame(
    data_store.dates,
    columns=['date', 'value']
  )
  
  date_range = pd.to_datetime(df['date']).dt
  week = date_range.isocalendar().week
  
  df['date'] = date_range
  df['month'] = date_range.month.map(lambda x: calendar.month_abbr[x])
  df['year'] = date_range.year
  df["weekday"] = date_range.weekday.map(lambda x: calendar.day_abbr[x])
  df["week"] = week.where(~((week > 5) & (date_range.month == 1)), 0)
  
  df_pivot = df.pivot_table(
    index=['year', 'weekday'],
    columns=['week'],
    values=['value'],
    aggfunc='first'
  )
  
  df_pivot.columns = pd.MultiIndex.from_frame(
    df[['month', 'week']].groupby('week').agg('first').reset_index()[['month', 'week']])
  content = [
    [
      dbc.Col(
        custom_head_lines.h3(year_selected),
        width=12,
      ),
      dbc.Col(
        create_table(df_pivot, year_selected),
        class_name="overflow-auto",
        width=12,
      ),
    ]
    for year_selected in df['year'].drop_duplicates().sort_values()
  ]
  
  return dbc.Container(
    dbc.Row(
      children=[*chain(*content)]
    )
  )
