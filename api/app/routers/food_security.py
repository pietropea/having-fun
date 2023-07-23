import time

from fastapi import APIRouter, HTTPException, Response, status

from ..calculations import calculate_average_metrics, calculate_national_daily_fcs
from ..data_source import data_source
from ..exceptions import ThirdPartyAPIIntegrationException
from ..logging import debug, info
from .. import schemas
from .. import config

router = APIRouter(prefix="/food_security", tags=["Food Security"])


@router.get(
    "/averages/{iso3}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MetricAResponse,
)
async def get_average_metrics(
    iso3: str,
    date_start: str = config.DEFAULT_DATE_START,
    date_end: str = config.DEFAULT_DATE_END,
):
    # TODO: configure proper app profiler
    api_invocation_timestamp = time.time()
    info(f"get_average_metrics API invoked at: {api_invocation_timestamp}")

    try:
        data = await data_source.get_data(iso3, date_start, date_end)
        data_returned_timestamp = time.time()
        data_retrieval_time = data_returned_timestamp - api_invocation_timestamp
        info(f"Data returned in: {data_returned_timestamp - api_invocation_timestamp}")

    except ThirdPartyAPIIntegrationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exception.message
        )

    response = await calculate_average_metrics(data)
    # Profiling information
    calculation_completed_timestamp = time.time()
    data_processing_elapsed_time = (
        calculation_completed_timestamp - data_returned_timestamp
    )
    api_total_execution_time = (
        calculation_completed_timestamp - api_invocation_timestamp
    )
    info(
        f"Calculation completed at: {calculation_completed_timestamp} (took {data_processing_elapsed_time})"
    )
    info(
        f"Percentage of time spent retrieving data: {round(data_retrieval_time / api_total_execution_time * 100, 6)}"
    )
    info(
        f"Percentage of time spent processing data: {round(data_processing_elapsed_time / api_total_execution_time * 100, 6)}"
    )

    return schemas.MetricAResponse(country=response.country, regions=response.regions)


@router.get(
    "/daily_fcs/{iso3}/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MetricBResponse,
)
async def get_national_daily_fcs(
    iso3: str,
    date_start: str = "2022-06-01",
    date_end: str = "2023-07-01",
    include_variance: str = "false",
):
    # TODO: configure proper app profiler
    api_invocation_timestamp = time.time()
    info(f"get_national_daily_fcs API invoked at: {api_invocation_timestamp}")

    try:
        data = await data_source.get_data(iso3, date_start, date_end)
        data_returned_timestamp = time.time()
        data_retrieval_time = data_returned_timestamp - api_invocation_timestamp
        info(f"Data returned in: {data_retrieval_time}")

    except ThirdPartyAPIIntegrationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exception.message
        )

    result = await calculate_national_daily_fcs(
        data, include_variance.lower() == "true"
    )

    # Profiling information
    calculation_completed_timestamp = time.time()
    data_processing_elapsed_time = (
        calculation_completed_timestamp - data_returned_timestamp
    )
    api_total_execution_time = (
        calculation_completed_timestamp - api_invocation_timestamp
    )
    info(
        f"Calculation completed at: {calculation_completed_timestamp} (took {data_processing_elapsed_time})"
    )
    info(
        f"Percentage of time spent retrieving data: {round(data_retrieval_time / api_total_execution_time * 100, 6)}"
    )
    info(
        f"Percentage of time spent processing data: {round(data_processing_elapsed_time / api_total_execution_time * 100, 6)}"
    )

    return schemas.MetricBResponse(
        country=result.country,
        fcs_prevalence=result.fcs_prevalence,
        variance=result.variance,
    )
