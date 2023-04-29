from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ParseError

from aws_lambda_powertools import Logger
from kink import inject

from src.errors import ErrorParsingXMLData


@inject
def parse_xml_rates(xml_doc: str, logger: Logger) -> (str, dict):
    try:
        root = ET.fromstring(xml_doc)
        ns = {"ns": root.findall("*")[-1].tag.split("}")[0][1:]}
        rates_date = root.find("ns:Cube/ns:Cube", ns).attrib["time"]
        currencies = {}
        for child in root.find("ns:Cube/ns:Cube", ns):
            currencies[child.attrib["currency"]] = float(child.attrib["rate"])
    except ParseError as e:
        description = "Error parsing fetched currencies"
        logger.error(description)
        raise ErrorParsingXMLData(description) from e

    return rates_date, currencies
