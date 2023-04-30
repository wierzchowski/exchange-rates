import json

from src.handlers.show_rates import handle as show_rates_handler


def test_show_rates_with_diff(dynamodb_resource, lambda_context):
    table = dynamodb_resource.Table("exchange-rates-rates-table")
    table.put_item(
        Item={
            "kind": "rates",
            "date": "2000-01-01",
            "rates": json.dumps({"USD": 1.0981, "GBP": 0.8805, "PLN": 4.5815}),
        }
    )
    table.put_item(
        Item={
            "kind": "rates",
            "date": "2000-01-02",
            "rates": json.dumps({"USD": 1.0911, "GBP": 0.8905, "PLN": 4.5815}),
        }
    )

    response = show_rates_handler(event={}, context=lambda_context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {
        "rates_date": "2000-01-02",
        "rates_diff_date": "2000-01-01",
        "rates": {
            "USD": {"rate": 1.0911, "diff": -0.007},
            "GBP": {"rate": 0.8905, "diff": 0.01},
            "PLN": {"rate": 4.5815, "diff": 0.0},
        },
    }


def test_show_rates_with_no_diff(dynamodb_resource, lambda_context):
    table = dynamodb_resource.Table("exchange-rates-rates-table")
    table.put_item(
        Item={
            "kind": "rates",
            "date": "2000-01-01",
            "rates": json.dumps({"USD": 1.0981, "GBP": 0.8805, "PLN": 4.5815}),
        }
    )

    response = show_rates_handler(event={}, context=lambda_context)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {
        "rates_date": "2000-01-01",
        "rates": {
            "USD": {"rate": 1.0981},
            "GBP": {"rate": 0.8805},
            "PLN": {"rate": 4.5815},
        },
    }


def test_show_rates_empty_table(dynamodb_resource, lambda_context):
    response = show_rates_handler(event={}, context=lambda_context)

    assert response["statusCode"] == 204
    assert response["body"] == ""
