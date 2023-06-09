# generate using https://github.com/mingrammer/diagrams
# (there is dependency on Graphviz, most probably you will need to install it)
#
# cd adr/resources
# python3 001-diagram.py

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server

with Diagram(name="Currency rates", filename="001-diagram", show=False):
    user = Client("User")
    ecb = Server("ECB")

    with Cluster("AWS"):
        apigw = APIGateway("HTTP API")
        show_lambda = Lambda("exchange-rates-show-rates")
        fetch_lambda = Lambda("exchange-rates-fetch-rates \n(triggered daily)")
        dynamo = Dynamodb("exchange-rates-rates-table")

    user >> apigw >> show_lambda << dynamo
    user << Edge(label="cache") << apigw << show_lambda

    ecb << fetch_lambda >> dynamo
    ecb >> fetch_lambda
