import pytest

from src.errors import ErrorParsingXMLData
from src.helpers.xml import parse_xml_rates


def test_xml(xml_rates, currencies_dict):
    date, currencies = parse_xml_rates(xml_rates)

    assert currencies == currencies_dict


@pytest.mark.parametrize(
    "string,error",
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
def test_xml_invalid_input(xml_rates, string, error):
    with pytest.raises(error):
        parse_xml_rates(string)
