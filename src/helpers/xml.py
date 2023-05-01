from defusedxml import ElementTree as ET
from xml.etree.ElementTree import Element, ParseError

from aws_lambda_powertools import Logger
from kink import inject

from src.errors import ErrorParsingXMLData
from src.helpers.models import DailyRate


class EcbXmlExtractor:
    @inject
    def __init__(self, xml_data: str, logger: Logger) -> None:
        self.xml_data = xml_data
        self.logger = logger
        self.root = self._get_root()
        self.ns = self._get_namespace()

    def get_currency_data(self, limit: int = 1) -> list[DailyRate]:
        rates = []
        for count, element in enumerate(self.root.findall("ns:Cube/ns:Cube", self.ns)):
            if count >= limit:
                break
            rates.append(
                DailyRate(
                    date=self._extract_date(element),
                    rates=self._extract_currencies(element),
                )
            )
        return rates

    def _get_root(self) -> Element:
        try:
            return ET.fromstring(self.xml_data)
        except ParseError as e:
            description = "Error getting document root"
            self.logger.error(description)
            raise ErrorParsingXMLData(description) from e

    def _extract_currencies(self, node: Element) -> dict[str, float]:
        try:
            currencies = {}
            for child in node:
                currencies[child.attrib["currency"]] = float(child.attrib["rate"])
            return currencies
        except ParseError as e:
            description = "Error parsing fetched currencies"
            self.logger.error(description)
            raise ErrorParsingXMLData(description) from e

    def _extract_date(self, node: Element) -> str:
        return node.attrib["time"]

    def _get_namespace(self) -> dict[str, str]:
        return {"ns": self.root.findall("*")[-1].tag.split("}")[0][1:]}
