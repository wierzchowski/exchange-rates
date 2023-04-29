### Context
Currency rates will be fetched by AWS Lambda and served via HTTP trigger. Usage pattern is unknown.

### Solution
Dynamodb table is chosen with composite key - `rates` as partition key and `date` as sort key.
