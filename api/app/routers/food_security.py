import time

from fastapi import APIRouter, HTTPException, Response, status

from ..calculations import calculate_average_metrics, calculate_national_daily_fcs
from ..data_source import data_source
from ..exceptions import ThirdPartyAPIIntegrationException
from ..logging import debug
from .. import schemas
from .. import config

router = APIRouter(prefix="/food_security", tags=["Food Security"])


@router.get(
    "/averages/{iso3}/",
    status_code=status.HTTP_200_OK,
    # response_model=schemas.MetricAResponse,
)
def get_average_metrics(
    iso3: str,
    date_start: str = config.DEFAULT_DATE_START,
    date_end: str = config.DEFAULT_DATE_END,
):
    # TODO: configure proper app profiler
    start_timestamp = time.time()

    try:
        data = data_source.get_data(iso3, date_start, date_end)
        data_returned_timestamp = time.time()
        debug(f"Data returned in: {data_returned_timestamp - start_timestamp}")

    except ThirdPartyAPIIntegrationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exception.message
        )

    average_metrics_result, country = calculate_average_metrics(data)
    debug(f"Calculation completed at: {time.time() - data_returned_timestamp}")

    response = {"regions": average_metrics_result, "country": country}

    print(response)

    return response


@router.get(
    "/daily_fcs/{iso3}/",
    status_code=status.HTTP_200_OK,
    # response_model=schemas.MetricBResponse,
)
def get_national_daily_fcs(
    iso3: str,
    date_start: str = "2022-06-01",
    date_end: str = "2023-07-01",
    include_variance: str = "false",
):
    # TODO: configure proper app profiler
    start_timestamp = time.time()

    try:
        data = data_source.get_data(iso3, date_start, date_end)
        data_returned_timestamp = time.time()
        debug(f"Data returned in: {data_returned_timestamp - start_timestamp}")

    except ThirdPartyAPIIntegrationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=exception.message
        )

    average_metrics_result = calculate_national_daily_fcs(
        data, include_variance.lower() == "true"
    )
    debug(f"Calculation completed at: {time.time() - data_returned_timestamp}")

    return {"response": average_metrics_result}
