from logging import Logger

import requests
from kink import inject

from src.constants import EBC_RATES_URL
from src.errors import ErrorFetchingXMLData


class HttpClient:
    def __init__(self, logger: Logger, http_client: requests) -> None:
        self.logger = logger
        self.http_client = http_client

    def make_request(self, method: str, url: str) -> requests.Response:
        try:
            response = self.http_client.request(method=method, url=url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            description = "Connectivity issue while fetching data, status code = {response.status_code}"
            self.logger.error(description)
            raise ErrorFetchingXMLData(description) from e
        except requests.exceptions.HTTPError as e:
            description = f"Response issue while fetching data"
            self.logger.error(description)
            raise ErrorFetchingXMLData(description) from e
        return response


class EcbHttpClient(HttpClient):
    @inject
    def __init__(self, logger: Logger, http_client: requests) -> None:
        super().__init__(logger=logger, http_client=http_client)

    def get_current_rates_info(self) -> str:
        response = self.make_request(method="GET", url=EBC_RATES_URL)
        return response.text
