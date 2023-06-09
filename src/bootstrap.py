import boto3
import requests
from aws_lambda_powertools import Logger
from kink import di

from src.constants import SERVICE_NAME
from src.helpers.databases import RatesStorage
from src.helpers.http import EcbHttpClient


def bootstrap_di() -> None:
    di["logger"] = Logger(SERVICE_NAME, "INFO")
    di["http_client"] = requests
    di["dynamodb_resource"] = lambda _: boto3.resource("dynamodb")
    di[EcbHttpClient] = EcbHttpClient()
    di[RatesStorage] = lambda _: RatesStorage()
