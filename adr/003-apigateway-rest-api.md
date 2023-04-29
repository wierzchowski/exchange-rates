### Context
API Gateway provides 2 API types HTTP and REST API.

### Solution
API Gateway REST API is chosen, because it enables caching. Currency data changes once a day, 
so it will be worth to explore caching this data.
https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html
