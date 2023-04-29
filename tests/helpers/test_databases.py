from boto3.dynamodb.conditions import Key


def test_dynamodb(dynamodb_mocks, currencies_dict, rates_storage):
    client, resource = dynamodb_mocks
    table = resource.Table("exchange-rates-rates-table")

    rates_storage.put_rates("2022-12-31", currencies_dict)

    response = table.query(
        KeyConditionExpression=Key("kind").eq("rates") & Key("date").eq("2022-12-31")
    )
    assert len(response["Items"]) == 1
