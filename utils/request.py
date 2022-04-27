import logging
import requests

logger: logging.Logger = logging.getLogger(__name__)

ROOT_URL = "https://www.alphavantage.co/query"


class AlphaVantageQuery:
    def __init__(self, api_key: str, alpha_vantage_function: str):
        self.api_key = api_key
        self.alpha_vantage_function = alpha_vantage_function.upper()

    def get_request(self, params: dict) -> requests.models.Response:
        params.update({"apikey": self.api_key, "function": self.alpha_vantage_function})
        try:
            response: requests.models.Response = requests.get(ROOT_URL, params=params)
        except requests.Timeout as error_timeout:
            logger.error(f"{error_timeout}")
        except requests.HTTPError as error_http:
            logger.error(f"{error_http}")
        except requests.ConnectionError as error_connection:
            logger.error(f"{error_connection}")
        except requests.RequestException as error_request:
            logger.error(f"{error_request}")
        except Exception as error_unkown:
            logger.error(f"Unkown Error - {error_unkown}")
        else:
            if not response.ok:
                logger.error(f"Response Headers - {response.headers}")
                logger.error(f"Status Code - {response.status_code}")
                logger.error(f"Response - {response.json()}")
                raise ConnectionError("Exiting due to bad connection.")
            else:
                logger.info(f"Returning response from [{response.url}]")
                return response
