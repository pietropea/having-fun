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
    ThirdPartyAPINotAvailableException,
)
from .logging import info, err, debug
from typing import List
from .schemas import DataObject
from . import config
import aiohttp
import asyncio
from retry import retry


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

        # TODO: add validation if date_end after date_start date
        # if is_date_after(date_end, date_start):
        #     raise DateEndBeforeDateStartException

        # TODO: add validation if range too big validation

        return f"{config.THIRD_PARTY_API_BASE_URL}/v1/foodsecurity/country/{iso3}/region?date_start={date_start}&date_end={date_end}"

    @retry(ThirdPartyAPINotAvailableException, delay=3, tries=3)
    async def __perform_http_call(self, url) -> List[DataObject]:
        """
        Function to perform the actual HTTP request.
        The function implements a retry logic, max 3 retries with 3 sec of delay
        to make the integration stronger.
        Sometimes, the Third-party API returns a response body containing the error below.
        {'ErrorCode': 'ResourceExhausted', 'ErrorMessage': 'Function concurrent request count exceeded'}

        Args:
            url (str): The URL to call

        Returns:
            List[DataObject]: The response of the API call
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_json = await response.json()

                try:
                    if type(response_json) != list:
                        info("Third-Party API not available. Retrying...")
                        raise ThirdPartyAPINotAvailableException
                except Exception as error:
                    raise

                return response_json

    async def get_data(
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
        info(f"Get data for iso3={iso3}, date_start={date_start}, date_end={date_end}")
        try:
            url = self.__get_url(iso3, date_start, date_end)
            info(f"API URL: {url}")

            tasks = [self.__perform_http_call(url)]
            results = await asyncio.gather(*tasks)

            response_json = results[0]
            info(f"Data returned successfully")
            debug(response_json)

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
