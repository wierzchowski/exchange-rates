import pytest

from src.errors import ErrorParsingXMLData
from src.helpers.xml import EcbXmlExtractor


def test_xml(xml_rates, currencies_dict, daily_rate):
    extractor = EcbXmlExtractor(xml_rates)
    rates_list = extractor.get_currency_data()

    assert rates_list == [daily_rate]


@pytest.mark.parametrize(
    "invalid_xml_rates,error",
    (
        (
            "dummy string",
            ErrorParsingXMLData,
        ),
        (
            '<?xml version="1.0" encoding="UTF-8"?>',
            ErrorParsingXMLData,
        ),
    ),
)
def test_xml_invalid_input(invalid_xml_rates, error):
    with pytest.raises(error):
        extractor = EcbXmlExtractor(invalid_xml_rates)
        extractor.get_currency_data()
