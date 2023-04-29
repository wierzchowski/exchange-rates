from unittest.mock import Mock

import pytest
import requests
import responses
from requests.exceptions import ConnectionError, HTTPError

from src.errors import ErrorFetchingXMLData
from src.helpers.http import EBC_RATES_URL


@responses.activate
def test_xml_fetching_status_code_check(ecb_http_client, xml_rates):
    responses.add(responses.GET, EBC_RATES_URL, body=xml_rates, status=200)

    xml_data = ecb_http_client.get_current_rates_info()

    assert xml_data == xml_rates


@pytest.mark.parametrize("res_exception", ((ConnectionError,), (HTTPError,)))
def test_xml_fetching_issues(res_exception, ecb_http_client):
    with pytest.raises(ErrorFetchingXMLData):
        ecb_http_client.http_client = Mock(spec_set=requests)
        ecb_http_client.http_client.request.side_effect = res_exception

        ecb_http_client.get_current_rates_info()
