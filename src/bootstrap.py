import boto3
import requests
from aws_lambda_powertools import Logger
from kink import di

from src.helpers.databases import RatesStorage
from src.helpers.http import ECBHttpClient


def bootstrap_di() -> None:
    di["logger"] = Logger("exchange-rates")
    di["http_client"] = requests
    di["dynamodb_resource"] = lambda _: boto3.resource("dynamodb")
    di["ecb_http_client"] = ECBHttpClient()
    di["rates_storage"] = RatesStorage()
