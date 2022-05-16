from flask import Flask
from flask_graphql import GraphQLView
import graphene
import argparse
from argparse import ArgumentParser
from python_mock_trying.PgSqlExample_Declarative.schema import Query as query_cmp
from python_mock_trying.PgSqlExample_Declarative.database_connection import db_session
from python_mock_trying.observability.logging import setup_logger
from python_mock_trying.observability.apm_agent import setup_apm_agent
from loguru import logger
import elasticapm
from python_mock_trying.env import (
    APM_CONFIG,
)
import nanoid

class Query(query_cmp, graphene.ObjectType):
    pass

def get_args() -> argparse.Namespace:
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", help=("flask server port default at 5000"), type=int, default=5000)
    parser.add_argument("-d", "--debug", help=("flask server in debug mode"), type=bool, default=False)

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = get_args()
    # service config
    service_id = nanoid.generate()
    service_name = "MockTry"
    service_version = "1.0.0"

    setup_apm_agent(service_name, APM_CONFIG)
    setup_logger(service_name, service_id)
    # config Gql
    schema = graphene.Schema(query=Query)

    # config flask server
    app = Flask(__name__)
    app.debug = True
    app.add_url_rule("/graphql"
                     , view_func=GraphQLView.as_view("graphql"
                                                     , schema=schema))
    app.add_url_rule("/graphiql"
                     , view_func=GraphQLView.as_view("graphiql"
                                                     , schema=schema
                                                     , graphiql=True))
    app.run()
    db_session.remove()
