### Project scope

Currency exchange tracking application in the AWS lambda environment.  The application relies on 
[European Central Bank Data](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html). 
Exchange rates are fetched every day and stored in a DynamoDB table. The application exposes a public REST API endpoint 
that provides current exchange rate information for all tracked currencies and their change compared to the previous day 
for all the tracked currencies.

### Deployment

This project is based on [poetry](https://python-poetry.org/) and [serverless framework](https://www.serverless.com/).

```commandline
serverless deploy --region eu-west-1
```

Fill database with the latest records:

```commandline
serverless invoke -f storeRates --data '{"limit": 5}' --region eu-west-1
```

### Caveats

`Store events` Lambda function partially bases on event received. If triggered with empty event - reloads only newest 
rates from ECB, however if `limit` passed in an event - such amount of days is being loaded into DynamoDB.
