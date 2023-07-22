from . import schemas
import re

# Convert python ENUM in list of string
allowed_iso3_codes = [member.value for member in schemas.AllowedCountriesByISO3]


def is_valid_date_format(date: str) -> bool:
    """
    Auxiliary function to check if the provided string date uses
    the correct format.

    Args:
        date (str): The string representation of the date

    Returns:
        bool: Weather or not the date string is a valid date format
    """
    date_format_regex = re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")

    return bool(re.match(date_format_regex, date))


def is_date_after(date_start: str, date_end: str) -> bool:
    """
    Auxiliary function to check if the first argument date is
    after the second argument.

    Args:
        date_start (str): First date to use in the comparison
        date_end (str): Second date to use in the comparison

    Returns:
        bool: Weather the first date is after the second one
    """
    return date_start > date_end


def is_valid_iso3(iso3_code: str) -> bool:
    """
    Auxiliary function to check if the provided ISO3 code
    is supported by the application.

    Args:
        iso3_code (str): the ISO3 code to use

    Returns:
        bool: Weather or not the ISO3 code is supported.
    """
    return iso3_code in allowed_iso3_codes
