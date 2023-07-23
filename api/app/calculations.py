from typing import List, Any
from .schemas import (
    DataObject,
    CountryDataObject,
    RegionDataObject,
    AverageMetrics,
    CalculateAverageMetrics,
    FCSPrevalence,
    RegionMonthlyAverageMetrics,
    CalculateNationalDailyFCS,
)
from .logging import debug, info


async def calculate_average_metrics(data: List[Any]) -> CalculateAverageMetrics:
    info(f"calculate_average_metrics invocation with {len(data)} items")
    ###### ----- Preprocessing and data preparation
    # Dictionary to store the cumulative sum and count of metrics for each ADM1 area per month
    metrics_sum: dict[str, dict] = {}

    # Look up table for the ADM1 areas and regions
    adm1_areas: dict[str, RegionDataObject] = {}

    # Get the country information to enrich the API response
    debug("First data item returned")
    debug(data[0])
    first_data_object = DataObject(**data[0])
    country: CountryDataObject = first_data_object.country

    # Loop through the data to calculate the sum of metrics for each ADM1 area
    for raw_entry in data:
        entry = DataObject(**raw_entry)
        # Extract data values from each data object
        region: RegionDataObject = entry.region
        region_id = str(region.id)
        date = entry.date
        month = date[0:7]

        metrics = entry.metrics
        fcs_metric = metrics.fcs
        rcsi_metric = metrics.fcs
        market_access_metric = metrics.marketAccess

        # Initialize the region_id.month object is not present in the "metrics_sum" dictionary
        if region_id not in metrics_sum:
            metrics_sum[region_id] = {}

        if month not in metrics_sum[region_id]:
            metrics_sum[region_id][month] = {
                "fcs": 0,
                "rcsi": 0,
                "marketAccess": 0,
                "count": 0,
            }

        # Alias to the metrics_sum[region_id][month] object, just for readability
        region_id_month = metrics_sum[region_id][month]

        # Sum of each metric for the given region, in the processed month
        region_id_month["fcs"] += fcs_metric.prevalence
        region_id_month["rcsi"] += rcsi_metric.prevalence
        region_id_month["marketAccess"] += market_access_metric.prevalence

        # Count of considered metric values
        region_id_month["count"] += 1

        # Save the "region" information in the lookup table.
        if region_id not in adm1_areas:
            adm1_areas[region_id] = region

    ###### ----- Result generation
    # Dictionary to store the average metrics for each ADM1 area, for every month
    average_metrics_response: List[RegionMonthlyAverageMetrics] = []

    # Loop through ADM1 areas and the months to calculate the monthly average metrics
    for region_id in metrics_sum:
        months: List[AverageMetrics] = []
        for month in metrics_sum[region_id]:
            region_id_month = metrics_sum[region_id][month]
            count = region_id_month["count"]

            # Calculate the average for each metric
            calculated_metrics = AverageMetrics(
                fcs=float(region_id_month["fcs"] / count),
                rcsi=float(region_id_month["rcsi"] / count),
                marketAccess=float(region_id_month["marketAccess"] / count),
            )
            months.append(calculated_metrics)

        region_info = RegionMonthlyAverageMetrics(
            region=adm1_areas[region_id], months=months
        )
        average_metrics_response.append(region_info)

    return CalculateAverageMetrics(regions=average_metrics_response, country=country)


def extract_FCS_prevalence(entry: DataObject) -> float:
    # Extract data values
    metrics = entry.metrics
    fcs_metric = metrics.fcs
    fcs = fcs_metric.prevalence
    return fcs


def calculate_variance(data: List[Any]) -> float:
    # More info at: https://en.wikipedia.org/wiki/Variance
    # Steps to calculate:
    # 1. Calculate the set average
    total_sum = 0.0
    for raw_entry in data:
        entry = DataObject(**raw_entry)
        fcs = extract_FCS_prevalence(entry)
        total_sum += fcs

    days_amount = len(data)
    daily_metric_average = total_sum / days_amount

    # 2. Sum the power of 2 of the difference between the item's value and the list average
    sum_of_powers = 0.0
    for raw_entry in data:
        entry = DataObject(**raw_entry)
        fcs = extract_FCS_prevalence(entry)
        sum_of_powers += (fcs - daily_metric_average) ** 2

    # 3. Divide the sum of the powers by the list length
    # Subtract 1 "days_amount" to calculate the variance of a sample (variance = sum_of_powers / days_amount - 1)
    variance = sum_of_powers / days_amount

    return variance


async def calculate_national_daily_fcs(
    data: List[Any], include_variance: bool = False
) -> CalculateNationalDailyFCS:
    info(f"calculate_national_daily_fcs fn invoked with {len(data)} items")
    ###### ----- Preprocessing and data preparation
    # Dictionary to store the cumulative sum of FCS metrics for each ADM1 area
    daily_metrics_sum: dict[str, float] = {}
    # Get the country information to enrich the API response
    debug("First data item returned")
    debug(data[0])
    first_data_object = DataObject(**data[0])
    country: CountryDataObject = first_data_object.country

    # Loop through the data to calculate the sum of metrics for each ADM1 area
    for raw_entry in data:
        entry = DataObject(**raw_entry)
        # Extract data values
        date = entry.date
        metrics = entry.metrics
        fcs_metric = metrics.fcs
        fcs = fcs_metric.prevalence

        # Initialize the date object is not present
        if date not in daily_metrics_sum:
            daily_metrics_sum[date] = 0

        daily_metrics_sum[date] += fcs

    ###### ----- Result generation
    fcs_prevalence_list: List[FCSPrevalence] = []
    for date in daily_metrics_sum:
        daily_metric = FCSPrevalence(date=date, prevalence=daily_metrics_sum[date])
        fcs_prevalence_list.append(daily_metric)

    response = CalculateNationalDailyFCS(
        country=country,
        fcs_prevalence=fcs_prevalence_list,
        variance=None,
    )

    # Optionally include variance calculation
    if include_variance:
        # Include variance in the response
        response.variance = calculate_variance(data)

    return response
