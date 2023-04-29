import json

from aws_lambda_powertools.utilities.typing import LambdaContext


def handle(event: dict, context: LambdaContext) -> dict:
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({"some": "values"}),
    }
