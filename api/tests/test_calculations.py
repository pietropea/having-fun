import pytest
from app.calculations import calculate_variance


@pytest.fixture()
def data():
    return [
        {
            "country": {"id": 57, "name": "Colombia", "iso3": "COL", "iso2": "CO"},
            "region": {"id": 901156, "name": "Antioquia", "population": 6226346},
            "date": "2023-06-01",
            "dataType": "SURVEY",
            "metrics": {
                "fcs": {"people": 1752566, "prevalence": 0.28147612621716694},
                "rcsi": {"people": 2119672, "prevalence": 0.3404359475043629},
                "marketAccess": {"people": 2625245, "prevalence": 0.5225892504339518},
            },
        },
        {
            "country": {"id": 57, "name": "Colombia", "iso3": "COL", "iso2": "CO"},
            "region": {"id": 901157, "name": "Atl\u00e1ntico", "population": 2420044},
            "date": "2023-06-01",
            "dataType": "SURVEY",
            "metrics": {
                "fcs": {"people": 750494, "prevalence": 0.3101158491333215},
                "rcsi": {"people": 887091, "prevalence": 0.3665598642008162},
                "marketAccess": {"people": 1065133, "prevalence": 0.515748671107132},
            },
        },
        {
            "country": {"id": 57, "name": "Colombia", "iso3": "COL", "iso2": "CO"},
            "region": {
                "id": 901158,
                "name": "Bogot\u00e1, D.c.",
                "population": 7899968,
            },
            "date": "2023-06-01",
            "dataType": "SURVEY",
            "metrics": {
                "fcs": {"people": 2223651, "prevalence": 0.281476231758562},
                "rcsi": {"people": 2689433, "prevalence": 0.3404359359430317},
                "marketAccess": {"people": 3330903, "prevalence": 0.5225893280002629},
            },
        },
    ]


def test_calculate_variance(data):
    assert calculate_variance(data) == 0.0002734102353496459
