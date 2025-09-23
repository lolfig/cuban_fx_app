# build-in
import datetime

# packages
import httpx
from httpx import HTTPError

from services import formaters
# framework
from services.framework_scraping.tools import const, types


async def fetch_messages(currency: str, start_moment: datetime.datetime,
                         end_moment: datetime.datetime) -> types.MessagesStep:
  """
  Downloads raw offer messages from the TOQUE website based on a specified currency and date range.

  Args:
      currency (str): The currency for which messages are to be downloaded.
      start_moment (datetime.datetime): The start date for fetching messages (inclusive).
      end_moment (datetime.datetime): The end date for fetching messages (inclusive).

  Returns:
      MessagesStep: A dataclass containing the raw messages fetched.
  
  Raises:
      HTTPError: If the HTTP request fails.
      Exception: For any other errors during the fetching process.
  """
  start_str, end_str = formaters.datetime_to_str(start_moment), formaters.datetime_to_str(end_moment)
  
  print(f"Fetching data for {end_str}")
  try:
    # Espera hasta adquirir el lock (mutua exclusión con otros scrapers)
    from services.framework_scraping.locks import AsyncFileLock, DEFAULT_LOCK_PATH
    async with AsyncFileLock(DEFAULT_LOCK_PATH, poll_interval=0.5, timeout=None):
      async with httpx.AsyncClient() as client:
        response = await client.get(
          f"{const.SOURCE_URL}?" + "&".join(
            [
              f"token={const.ACCESS_TOKEN}",
              f"date_from={start_str}%2000:00:00",
              f"date_to={end_str}%2000:00:00"
            ]
          ), timeout=5
        )
        response.raise_for_status()
        messages = response.json()["statistics"][currency]["messages"]
      
      return types.MessagesStep(
        end=end_str,
        start=start_str,
        messages=messages
      )
  except HTTPError as error:
    print(f"HTTP error occurred: {error!r}")  # Usar !r para mostrar la representación completa
    if hasattr(error, 'response') and error.response is not None:
        print("Response content:", error.response.text)
    raise ConnectionError("Failed to fetch messages") from error
  except Exception as error:
    print(f"An error occurred: {error}")
    raise Exception("An error occurred while fetching messages") from error


async def fetch_exchange_rate_data(api_url: str):
  """
  Downloads exchange rate data from the specified API URL.

  Args:
      api_url (str): The API endpoint for fetching exchange rate data.

  Raises:
      ValueError: If the API response is empty or invalid.

    Returns:
        Dict[str, Any]: A dictionary containing the exchange rate data.
    """
  try:
    async with httpx.AsyncClient() as client:
      response = await client.get(api_url, timeout=5)
      response.raise_for_status()
      data = response.json()
    if not data:
      raise ValueError("API response is empty")
    return data
  except (HTTPError, ValueError) as e:
    print(f"Error fetching exchange rate data: {e}")
    raise ConnectionError("Failed to fetch exchange rate data") from e
  except Exception as error:
    print(f"An error occurred: {error}")
    raise Exception("An error occurred while fetching messages") from error