class InvalidDateException(Exception):
    "Raised when the input date follows an invalid format"

    def __init__(self, message) -> None:
        self.message = f"[{message}] invalid date format. Expected format YYYY-MM-DD"
        super().__init__(self.message)


class DateEndBeforeDateStartException(Exception):
    "Raised when the date_end is before date_start"
    pass


class DateRangeTooBigException(Exception):
    "Raised when the date_start and date_start are more than 500 days away"
    pass


class InvalidISO3Exception(Exception):
    "Raised when the input iso3 is not supported"
    pass


class ThirdPartyAPIIntegrationException(Exception):
    "Raised when the third-party API request fails"

    def __init__(self, message="Generic error") -> None:
        self.message = f"{message}"
        super().__init__(self.message)


class ThirdPartyAPINotAvailableException(Exception):
    "Raised when Third-Party API does not respond correctly"
    pass
