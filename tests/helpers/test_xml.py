import pytest

from src.errors import ErrorParsingXMLData
from src.helpers.models import DailyRate
from src.helpers.xml import EcbXmlExtractor


def test_xml_extract_success(xml_rates, currencies_dict, daily_rate):
    extractor = EcbXmlExtractor(xml_rates)
    rates_list = extractor.get_currency_data()

    assert rates_list == [daily_rate]


def test_xml_limit_higher_than_days_count(xml_rates, currencies_dict, daily_rate):
    extractor = EcbXmlExtractor(xml_rates)
    rates_list = extractor.get_currency_data(limit=5)

    assert rates_list == [
        DailyRate(
            date="2023-04-28", rates={"USD": 1.0981, "GBP": 0.8805, "PLN": 4.5815}
        ),
        DailyRate(
            date="2023-04-27", rates={"USD": 1.0911, "GBP": 0.8905, "PLN": 4.5815}
        ),
    ]


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
        (
            '<?xml version="1.0" encoding="UTF-8"?><gesmes:Envelope xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref" xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01"><gesmes:subject>Reference rates</gesmes:subject><gesmes:Sender><gesmes:name>European Central Bank</gesmes:name></gesmes:Sender><Cube></Cube></gesmes:Envelope>',
            ErrorParsingXMLData,
        ),
        (
            '<?xml version="1.0" encoding="UTF-8"?><gesmes:Envelope xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref" xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01"><gesmes:subject>Reference rates</gesmes:subject><gesmes:Sender><gesmes:name>European Central Bank</gesmes:name></gesmes:Sender></gesmes:Envelope>',
            ErrorParsingXMLData,
        ),
        (
            '<?xml version="1.0" encoding="UTF-8"?><gesmes:Envelope xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref" xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01"></gesmes:Envelope>',
            ErrorParsingXMLData,
        ),
        (
            '<?xml version="1.0" encoding="UTF-8"?><gesmes:Envelope xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref"></gesmes:Envelope>',
            ErrorParsingXMLData,
        ),
        (
            '<?xml version="1.0" encoding="UTF-8"?><gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01"></gesmes:Envelope>',
            ErrorParsingXMLData,
        ),
        (
            '<?xml version="1.0" encoding="UTF-8"?><gesmes:Envelope></gesmes:Envelope>',
            ErrorParsingXMLData,
        ),
    ),
)
def test_xml_invalid_input(invalid_xml_rates, error):
    with pytest.raises(error):
        extractor = EcbXmlExtractor(invalid_xml_rates)
        extractor.get_currency_data()
