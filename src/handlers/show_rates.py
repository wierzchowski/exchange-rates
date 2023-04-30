import json

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from kink import inject

from src.helpers.databases import RatesStorage
from src.helpers.models import DailyRate


@inject
def handle(
    event: dict, context: LambdaContext, logger: Logger, rates_storage: RatesStorage
) -> dict:
    logger.set_correlation_id(context.aws_request_id)

    rates = rates_storage.get_newest_rates(limit=2)
    if not rates:
        return prepare_response(status_code=204)
    elif len(rates) == 1:
        rates_obj = DailyRate.from_dynamodb_item(rates[0])
        body = prepare_rates_diff_response(rates_obj)
        return prepare_response(body=json.dumps(body))
    else:
        body = prepare_rates_diff_response(
            base_rates=DailyRate.from_dynamodb_item(rates[0]),
            diff_rates=DailyRate.from_dynamodb_item(rates[1]),
        )
        return prepare_response(body=json.dumps(body))


def prepare_response(body: str = None, status_code: int = 200) -> dict:
    if body is None:
        body = ""

    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "headers": {},
        "body": body,
    }


def prepare_rates_diff_response(
    base_rates: DailyRate, diff_rates: DailyRate = None
) -> dict:
    response = {"rates_date": base_rates.date, "rates": {}}
    for currency, value in base_rates.rates.items():
        response["rates"][currency] = {
            "rate": value,
        }

    if diff_rates:
        response["rates_diff_date"] = diff_rates.date
        for currency, value in diff_rates.rates.items():
            response["rates"][currency]["diff"] = round(
                base_rates.rates[currency] - value, 4
            )

    return response
