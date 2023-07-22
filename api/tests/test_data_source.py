import pytest
from app.data_source import data_source
from app.exceptions import ThirdPartyAPIIntegrationException


@pytest.fixture()
def ds():
    return data_source


@pytest.fixture()
def iso3():
    return "COL"


@pytest.fixture()
def properly_formed_date():
    return "2022-06-01"


@pytest.fixture()
def malformed_date():
    return "20220601"


def test_malformed_date_start(ds, iso3, properly_formed_date, malformed_date):
    with pytest.raises(ThirdPartyAPIIntegrationException):
        ds.get_data(iso3, properly_formed_date, malformed_date)


def test_malformed_date_end(ds, iso3, properly_formed_date, malformed_date):
    with pytest.raises(ThirdPartyAPIIntegrationException):
        ds.get_data(iso3, malformed_date, properly_formed_date)
