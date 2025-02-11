import datetime
from typing import List

import pandas as pd

# const
from config.const import (
  CURRENCIES,
  DIR_DATA_MESSAGES
)
# framework
from services.framework_scraping.tools import fetcher


# types


def generate_orders(processed_data):
  """
  Generates formal orders from processed messages.

  This method filters the processed data to generate orders with constraints on size
  and price, ensuring only valid entries are processed into the order list.
  """
  return [
    {
      "size": int(j[1]) if j[1] != "" else 0,
      "sign": j[0],
      "price": float(j[3]) if j[3] != "" else 0.0,
    }
    for j in processed_data
    if isinstance(j, list)
       and len(j) > 0
       and (j[1] != "" and int(j[1]) < 10000)
       and (j[3] != "" and float(j[3]) < 500)
  ]


def save_data_info(date: datetime.datetime, messages, processed_data, orders):
  """
  Saves all processed information into a Parquet file.
  """
  date_str = date.strftime("%Y-%m-%d")
  
  processed_data_normalized = [
    item if isinstance(item, list) else [] for item in processed_data
  ]
  
  combined_df = pd.DataFrame(
    [messages.values.tolist(), processed_data_normalized, orders]
  ).T
  combined_df.rename(
    columns={0: "messages", 1: "processed_messages", 2: "orders"}, inplace=True
  )
  
  combined_df.to_parquet(
    f"{DIR_DATA_MESSAGES}/{date_str}.parquet", index=False, engine="pyarrow"
  )


class DataProcessing:
  def __init__(
    self, dates: List[str],
    currency: CURRENCIES
  ):
    self.dates = [
      datetime.datetime.strptime(date, "%Y-%m-%d")
      for date
      in dates
    ]
    
    self.currency = currency
  
  def do_process_messages(self):
    """
    Processes raw messages to generate orders and save all information.

    This method iterates over the end dates and utilizes helper methods to:
    - Fetch raw messages.
    - Convert them into a DataFrame.
    - Interpret and process the messages.
    - Generate formal orders from these messages.
    - Save the collected data into a parquet file.
    """
    for end_date in self.dates:
      start_date = end_date - datetime.timedelta(days=1)
      raw_messages = fetcher.fetch_messages(
        currency=self.currency,
        start_moment=start_date,
        end_moment=end_date
      )
      messages = pd.DataFrame(
        raw_messages.messages,
        columns=[raw_messages.end]
      )
      
      processed_data = [
        messages.interpret(message_str)
        for message_str
        in raw_messages.messages
      ]
      orders = generate_orders(processed_data)
      
      save_data_info(end_date, messages, processed_data, orders)
      
      yield end_date
