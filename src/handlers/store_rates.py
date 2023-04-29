from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from kink import inject

from src.helpers.databases import RatesStorage
from src.helpers.http import ECBHttpClient
from src.helpers.xml import parse_xml_rates


@inject
def handle(
    event: dict,
    context: LambdaContext,
    logger: Logger,
    rates_storage: RatesStorage,
    ecb_http_client: ECBHttpClient,
) -> None:
    logger.set_correlation_id(context.aws_request_id)
    logger.info("Fetching rates")
    xml_rates = ecb_http_client.get_current_rates_info()
    logger.info("Extracting rates")
    rates_date, rates = parse_xml_rates(xml_rates)
    logger.info("Storing rates")
    rates_storage.put_rates(rates_date, rates)
    logger.info("Rates successfully stored")
