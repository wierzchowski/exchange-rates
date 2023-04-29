import json
from unittest.mock import Mock

import boto3
import pytest
import requests
from aws_lambda_powertools import Logger
from moto import mock_dynamodb

from src.helpers.databases import RatesStorage
from src.helpers.http import ECBHttpClient


@pytest.fixture
def ecb_http_client() -> ECBHttpClient:
    return ECBHttpClient(logger=Mock(spec_set=Logger), http_client=requests)


@pytest.fixture
def rates_storage(dynamodb_mocks) -> RatesStorage:
    client, resource = dynamodb_mocks
    return RatesStorage(resource)


@pytest.fixture
def dynamodb_mocks(currencies_dict):
    with mock_dynamodb():
        client = boto3.client("dynamodb")
        resource = boto3.resource("dynamodb")

        client.create_table(
            TableName="exchange-rates-rates-table",  # TODO: can be prettier: sls output -> Lambda envs -> os.environ
            BillingMode="PAY_PER_REQUEST",
            AttributeDefinitions=[
                {"AttributeName": "kind", "AttributeType": "S"},
                {"AttributeName": "date", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "kind", "KeyType": "HASH"},
                {"AttributeName": "date", "KeyType": "RANGE"},
            ],
        )
        table = resource.Table("exchange-rates-rates-table")
        table.put_item(
            Item={
                "kind": "rates",
                "date": "2000-01-01",
                "rates": json.dumps(currencies_dict),
            }
        )

        yield client, resource


@pytest.fixture
def xml_rates() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01" xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">
	<gesmes:subject>Reference rates</gesmes:subject>
	<gesmes:Sender>
		<gesmes:name>European Central Bank</gesmes:name>
	</gesmes:Sender>
	<Cube>
		<Cube time='2023-04-28'>
			<Cube currency='USD' rate='1.0981'/>
			<Cube currency='GBP' rate='0.88050'/>
			<Cube currency='PLN' rate='4.5815'/>
		</Cube>
	</Cube>
</gesmes:Envelope>"""


@pytest.fixture
def currencies_dict() -> dict:
    return {"USD": 1.0981, "GBP": 0.8805, "PLN": 4.5815}
