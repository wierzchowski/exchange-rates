import os

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from kink import inject

from src.observability import tracer
from src.helpers.databases import RatesStorage
from src.helpers.http import EcbHttpClient
from src.helpers.xml import EcbXmlExtractor


@tracer.capture_lambda_handler(capture_response=False)
@inject
def handle(
    event: dict,
    context: LambdaContext,
    logger: Logger,
    rates_storage: RatesStorage,
    ecb_http_client: EcbHttpClient,
) -> str:
    logger.set_correlation_id(context.aws_request_id)

    if event.get("limit") and isinstance(event.get("limit"), int):
        limit = event.get("limit")
    else:
        limit = 1

    logger.info("Fetching rates")
    xml_rates = ecb_http_client.get_current_rates_info()
    logger.info("Extracting rates")
    extractor = EcbXmlExtractor(xml_rates)
    extracted_rates = extractor.get_currency_data(limit=limit)
    logger.info("Storing rates")
    for rates in extracted_rates:
        logger.debug(f"{rates.date = }")
        logger.debug(f"{rates.rates = }")
        rates_storage.put_rates(rates.date, rates.rates)
    logger.info("Rates successfully stored")

    if os.environ.get("APIGW_CACHED"):
        logger.info("Invalidating API Gateway cache")
        apigw_client = boto3.client('apigateway')
        response = apigw_client.flush_stage_cache(
            restApiId=os.environ.get("APIGW_ID"),
            stageName=os.environ.get("APIGW_STAGE")
        )
        logger.info(response)
        logger.info("API Gateway cache invalidated")

    return f"Successfully loaded {limit} item(s)"
