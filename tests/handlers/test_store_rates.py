import pytest
import responses
from boto3.dynamodb.conditions import Key

from src.constants import EBC_RATES_URL
from src.errors import NoNewRatesError
from src.handlers.store_rates import handle as store_rates_handler


@pytest.mark.parametrize(
    "event,db_response",
    (
        (
            {"input": 1},
            [
                {
                    "date": "2023-04-28",
                    "kind": "rates",
                    "rates": '{"USD": 1.0981, "GBP": 0.8805, "PLN": 4.5815}',
                }
            ],
        ),
        (
            {"limit": 5},
            [
                {
                    "date": "2023-04-28",
                    "kind": "rates",
                    "rates": '{"USD": 1.0981, "GBP": 0.8805, "PLN": 4.5815}',
                },
                {
                    "date": "2023-04-27",
                    "kind": "rates",
                    "rates": '{"USD": 1.0911, "GBP": 0.8905, "PLN": 4.5815}',
                },
            ],
        ),
    ),
)
@responses.activate
def test_store_rates(dynamodb_resource, xml_rates, lambda_context, event, db_response):
    table = dynamodb_resource.Table("exchange-rates-rates-table")
    responses.add(responses.GET, EBC_RATES_URL, body=xml_rates, status=200)

    store_rates_handler(event=event, context=lambda_context)

    response = table.query(
        KeyConditionExpression=Key("kind").eq("rates"),
        Limit=5,
        ScanIndexForward=False,
    )
    assert response["Items"] == db_response


def test_store_rates_no_new_rates_daily(dynamodb_resource, xml_rates, lambda_context):
    _ = dynamodb_resource.Table("exchange-rates-rates-table")
    responses.add(responses.GET, EBC_RATES_URL, body=xml_rates, status=200)

    with pytest.raises(NoNewRatesError):
        store_rates_handler(
            event={"limit": 1, "type": "daily-cron"}, context=lambda_context
        )
