# generate using https://github.com/mingrammer/diagrams
# (there is dependency on Graphviz, most probably you will need to install it)
#
# cd adr/resources
# python3 001-diagram.py

from diagrams import Cluster, Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server

with Diagram(name="Currency rates", filename="001-diagram", show=False):
    user = Client("User")
    ebc = Server("EBC")

    with Cluster("AWS"):
        apigw = APIGateway("HTTP API")
        apigw_lambda = Lambda("show_rates")
        event_lambda = Lambda("fetch rates \n(triggered daily)")
        dynamo = Dynamodb("Currency storage")

    user << apigw >> apigw_lambda << dynamo
    user >> apigw << apigw_lambda

    ebc << event_lambda >> dynamo
