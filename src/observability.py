from aws_lambda_powertools import Tracer

from src.constants import SERVICE_NAME


tracer = Tracer(SERVICE_NAME)
