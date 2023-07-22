from pydantic import BaseModel, RootModel
from enum import Enum
from typing import Dict, Optional


class AllowedCountriesByISO3(Enum):
    """
    Enumeration of the supported ISO3 codes
    """

    COLOMBIA = "COL"
    BURKINA_FASO = "BFA"


class MetricDataObject(BaseModel):
    people: int
    prevalence: float


class CountryDataObject(BaseModel):
    """
    Model that represent the Third-party API country model
    """

    id: int
    name: str
    iso3: str
    iso2: str


class RegionDataObject(BaseModel):
    """
    Model that represent the Third-party API sub-national (administrative level 1 ADM1 areas) model
    """

    id: int
    name: str
    population: int


class MetricsDataObject(BaseModel):
    """
    Model that represent the Third-party API metrics information for sub-national models
    """

    fcs: MetricDataObject
    rcsi: MetricDataObject
    marketAccess: MetricDataObject
    healthAccess: Optional[MetricDataObject] = None


class DataObject(BaseModel):
    """
    Model that represent the Third-party API response model
    """

    country: CountryDataObject
    region: RegionDataObject
    date: str
    dataType: str
    metrics: MetricsDataObject


class MetricAAreaMonthlyAverages(MetricsDataObject):
    """
    Model that represent the Metric A API response
    """

    region: RegionDataObject


# Model that represent the Metric A API response
class MetricAResponse(BaseModel):
    country: CountryDataObject
    regions: RootModel[Dict[str, Dict[str, MetricAAreaMonthlyAverages]]]
