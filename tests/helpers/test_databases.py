from boto3.dynamodb.conditions import Key


def test_dynamodb(dynamodb_resource, currencies_dict, rates_storage):
    table = dynamodb_resource.Table("exchange-rates-rates-table")

    rates_storage.put_rates("2022-12-31", currencies_dict)

    response = table.query(
        KeyConditionExpression=Key("kind").eq("rates") & Key("date").eq("2022-12-31")
    )
    assert len(response["Items"]) == 1
