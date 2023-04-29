import json


def handle(event: dict, context: dict) -> dict:
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({"some": "values"})
    }
