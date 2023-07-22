import requests
from .utils import (
    is_valid_date_format,
    is_valid_iso3,
    allowed_iso3_codes,
    is_date_after,
)
from .exceptions import (
    InvalidDateException,
    InvalidISO3Exception,
    ThirdPartyAPIIntegrationException,
    DateEndBeforeDateStartException,
)
from .logging import info, err
from typing import List
from .schemas import DataObject
from . import config


class DataSource:
    def __get_url(self, iso3: str, date_start: str, date_end: str) -> str:
        """
        Auxiliary function to generated to Third-Party API URL to invoke.
        The function also implements parameters validation based.

        Args:
            iso3 (str): ISO3 code to use in the Third-party API request
            date_start (str): "date_start" to use in the Third-party API request
            date_end (str): "date_end" to use in the Third-party API request

        Raises:
            InvalidDateException: When one of provided dates is not valid
            InvalidISO3Exception: When the provided ISO3 code is not valid

        Returns:
            str: The Third-party API formatted URL
        """
        if not is_valid_date_format(date_start):
            raise InvalidDateException("date_start")

        if not is_valid_date_format(date_end):
            raise InvalidDateException("date_end")

        if not is_valid_iso3(iso3):
            raise InvalidISO3Exception

        # TODO: add is date_end after date_start date
        # if is_date_after(date_end, date_start):
        #     raise DateEndBeforeDateStartException

        # TODO: add is range too big validation

        return f"{config.THIRD_PARTY_API_BASE_URL}/v1/foodsecurity/country/{iso3}/region?date_start={date_start}&date_end={date_end}"

    def get_data(
        self,
        iso3: str,
        date_start: str,
        date_end: str,
    ) -> List[DataObject]:
        """
        The function integrates with the Third-party API and returns
        the data according to the provided input parameters.

        Args:
            iso3 (str): ISO3 code to use in the Third-party API request
            date_start (str): "date_start" to use in the Third-party API request
            date_end (str): "date_end" to use in the Third-party API request

        Raises:
            ThirdPartyAPIIntegrationException: If the Third-party API request fails.

        Returns:
            List[DataObject]: The Third-party data.
        """
        info(
            f"Get data request with iso3={iso3}, date_start={date_start}, date_end={date_end}"
        )
        try:
            url = self.__get_url(iso3, date_start, date_end)
            info(f"API URL: {url}")

            response = requests.get(url)
            info(f"Data returned successfully")

            response_json = response.json()

            return response_json
        except InvalidDateException as exception:
            err(exception.message)
            raise ThirdPartyAPIIntegrationException(exception.message)
        except InvalidISO3Exception:
            error_message = (
                f"ISO3 code not supported. Supported codes: {allowed_iso3_codes}"
            )
            err(error_message)
            raise ThirdPartyAPIIntegrationException(error_message)
        except DateEndBeforeDateStartException:
            error_message = f"date_end is before date_start"
            err(error_message)
            raise ThirdPartyAPIIntegrationException(error_message)
        except:
            error_message = "Third-party API currently not available."
            err(error_message)
            raise ThirdPartyAPIIntegrationException(error_message)


data_source = DataSource()
