# python mock exampe for SQLalchemy
## Why we have this example
In this example, I would like to record:
- an example of postgres db, sqlalchemy and graphql
- an example of how to use python mock unittest with sqlalchemy

## Strucutre of this example
```mermaid
graph LR

A[user] --> |GraphQL Request| B(Flask GQL Server)
B --> C[GQL and SQLalchemy Handler]
C --> |Postgres Query| D(PG DB)
```
```mermaid
graph RL

A(PG DB) --> |Postgres Reply| B[json convertor]
B --> |json| C(Flask GQL Server)
C --> |GQL Reply| D[user]
```

## How to run this example
- Create the PG DB
  - One can use the docker compose example [here](https://github.com/SulfredLee/DailyProblem/tree/master/docker/postgresdb)
- Insert data into the DB. You can find the sql from files:
  - create_database.sql
  - insert_data.sql
- Prepare python by poetry
  - $ poetry install
- Start the web server
  - $ poetry run python python_mock_trying/web_app.py
- Visit the Graphiql page
  - [example link](http://localhost:5000/graphiql?query=query%20show_company_details%20%7B%0A%20%20showCompanyDetails(%0A%20%20%20%20company%3A%20%22OO%20Capital%22)%20%7B%0A%20%20%20%20name%0A%20%20%20%20department%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%20%20address%0A%20%20%20%20%20%20startTime%0A%20%20%20%20%20%20endTime%0A%20%20%20%20%20%20numberOfEmployee%0A%20%20%20%20%20%20employee%20%7B%0A%20%20%20%20%20%20%20%20name%0A%20%20%20%20%20%20%20%20gender%0A%20%20%20%20%20%20%20%20salary%0A%20%20%20%20%20%20%20%20isFullTime%0A%20%20%20%20%20%20%20%20department%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A%0Aquery%20show_employee_list%20%7B%0A%20%20showAllEmployee(%0A%20%20%20%20company%3A%20%22OO%20Capital%22%0A%20%20%20%20department%3A%20%22Management%22%0A%20%20)%20%7B%0A%20%20%20%20name%0A%20%20%20%20gender%0A%20%20%20%20department%0A%20%20%20%20company%0A%20%20%7D%0A%7D&operationName=show_company_details)
