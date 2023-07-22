from typing import List
from .schemas import DataObject, CountryDataObject, RegionDataObject


def calculate_average_metrics(data: List[DataObject]):
    ###### ----- Preprocessing and data preparation
    # Dictionary to store the cumulative sum and count of metrics for each ADM1 area per month
    metrics_sum: dict[str, dict] = {}

    # Look up table for the ADM1 areas info
    adm1_areas: dict[str, RegionDataObject] = {}

    # Get the country information to enrich the API response
    first_data_object: DataObject = data[0]
    country: CountryDataObject = first_data_object.country

    # Loop through the data to calculate the sum of metrics for each ADM1 area
    for entry in data:
        # Extract data values from each data object
        region = entry.region
        region_id = region.id
        date = entry.date
        month = date[0:7]

        metrics = entry.metrics
        fcs_metric = metrics.fcs
        fcs = fcs_metric.prevalence
        rcsi_metric = metrics.fcs
        rcsi = rcsi_metric.prevalence
        market_access_metric = metrics.marketAccess
        market_access = market_access_metric.prevalence

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
        region_id_month["fcs"] += fcs
        region_id_month["rcsi"] += rcsi
        region_id_month["marketAccess"] += market_access
        # Count of considered metric values
        region_id_month["count"] += 1

        # Save the "region" information in the lookup table.
        if region_id not in adm1_areas:
            adm1_areas[region_id] = region

    ###### ----- Result generation
    # Dictionary to store the average metrics for each ADM1 area, for every month
    average_metrics: dict[str, dict] = {}

    # Loop through ADM1 areas and the months to calculate the monthly average metrics
    for region_id in metrics_sum:
        for month in metrics_sum[region_id]:
            # Initialize the monthly average metrics result for the considered region_id/month
            if region_id not in average_metrics:
                average_metrics[region_id] = {}

            region_id_month = metrics_sum[region_id][month]
            count = region_id_month["count"]

            # Calculate the average for each metric
            average_metrics[region_id][month] = {
                "fcs": region_id_month["fcs"] / count,
                "rcsi": region_id_month["rcsi"] / count,
                "marketAccess": region_id_month["marketAccess"] / count,
                "region": region,
            }

    return (average_metrics, country)


def calculate_national_daily_fcs(
    data: List[DataObject], include_variance: bool = False
):
    ###### ----- Preprocessing and data preparation
    # Dictionary to store the cumulative sum of FCS metrics for each ADM1 area
    daily_metrics_sum: dict[str, float] = {}
    # Get the country information to enrich the API response
    first_data_object: DataObject = data[0]
    country: CountryDataObject = first_data_object.country

    # Loop through the data to calculate the sum of metrics for each ADM1 area
    for entry in data:
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
    response = {"country": country, "fcs_prevalence": daily_metrics_sum}

    # Optionally include variance calculation per day
    # More info at: https://en.wikipedia.org/wiki/Variance
    if include_variance:
        # Steps to calculate:
        # 1. Calculate the set average
        total_sum = 0.0
        for date in daily_metrics_sum:
            total_sum += daily_metrics_sum[date]

        days_amount = len(data)
        daily_metric_average = total_sum / days_amount

        # 2. Sum the power of 2 of the difference between the item's value and the list average
        sum_of_powers = 0.0
        for date in daily_metrics_sum:
            sum_of_powers += (daily_metrics_sum[date] - daily_metric_average) ** 2

        # 3. Divide the sum of the powers by the list length - 1
        variance = sum_of_powers / (days_amount - 1)

        # Include variance in the response
        response["variance"] = variance

    return response
