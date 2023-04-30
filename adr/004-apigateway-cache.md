### Context
Data in database changes once a day on working days - this leaves space to set up caching

### Solution
Implement caching in API Gateway. After loading data to database, API GW stage cache can be invalidated to serve fresh data. 
