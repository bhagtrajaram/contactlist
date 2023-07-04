import functools
from requests.exceptions import ConnectionError, RequestException

BASE_ERROR_MESSAGE = "could not connect to the datasource provider:{error_reason}"


def handle_connection_exception(func):
    """Decorator for handling exceptions."""

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
        except RequestException as e:
            error_reason = "some unknown error occured contacting your data-provider"
            if isinstance(e, ConnectionError):
                error_reason = "unknown data-provider"
            context = {
                "message": BASE_ERROR_MESSAGE.format(error_reason=error_reason),
            }
            response = context
        return response

    return wrapper
