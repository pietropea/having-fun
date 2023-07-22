from pydantic import BaseModel, RootModel
from enum import Enum
from typing import Dict, Optional, List


class AllowedCountriesByISO3(Enum):
    """
    Enumeration of the supported ISO3 codes
    """

    COLOMBIA = "COL"
    BURKINA_FASO = "BFA"


class MetricDataObject(BaseModel):
    people: int
    prevalence: float


class MetricsDataObject(BaseModel):
    """
    Model that represent the Third-party API metrics information for sub-national models
    """

    fcs: MetricDataObject
    rcsi: MetricDataObject
    marketAccess: MetricDataObject
    healthAccess: Optional[MetricDataObject] = None


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


class AverageMetrics(BaseModel):
    fcs: float
    rcsi: float
    marketAccess: float


class RegionMonthlyAverageMetrics(BaseModel):
    region: RegionDataObject
    months: List[AverageMetrics]


class CalculateAverageMetrics(BaseModel):
    country: CountryDataObject
    regions: List[RegionMonthlyAverageMetrics]


class MetricAResponse(CalculateAverageMetrics):
    pass


class FCSPrevalence(BaseModel):
    date: str
    prevalence: float


class CalculateNationalDailyFCS(BaseModel):
    country: CountryDataObject
    fcs_prevalence: List[FCSPrevalence]
    variance: Optional[float] = None


class MetricBResponse(CalculateNationalDailyFCS):
    pass
