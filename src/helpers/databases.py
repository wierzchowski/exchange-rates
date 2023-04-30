import json

from aws_lambda_powertools import Logger
from boto3 import resource
from botocore.exceptions import ClientError
from kink import inject

from src.errors import DynamoDBError


class RatesStorage:
    @inject
    def __init__(self, dynamodb_resource: resource, logger: Logger) -> None:
        self.resource = dynamodb_resource
        self.table = self.resource.Table(
            "exchange-rates-rates-table"
        )  # TODO: can be prettier: sls output -> Lambda envs -> os.environ
        self.logger = logger

    def put_rates(self, rates_date: str, rates: dict) -> None:
        try:
            response = self.table.put_item(
                Item={"kind": "rates", "date": rates_date, "rates": json.dumps(rates)}
            )
        except ClientError as e:
            description = "Error while saving rates to database"
            self.logger.error(description)
            raise DynamoDBError(description) from e

        response_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if response_code != 200:
            description = f"DynamoDB response status code {response_code}"
            self.logger.error(description)
            raise DynamoDBError(description)
