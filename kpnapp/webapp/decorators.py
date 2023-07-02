import functools

from django.shortcuts import render
from requests.exceptions import ConnectionError, RequestException


BASE_ERROR_MESSAGE = 'Could not connect to the datasource provider:{error_reason}'

def handle_view_exception(func):
    """Decorator for handling exceptions."""
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
        except RequestException as e:
            error_reason = 'Some unknown error occured contacting your data-provider'
            if isinstance(e, ConnectionError):
                error_reason = 'Unknown data-provider'
            context = {
              'message': BASE_ERROR_MESSAGE.format(error_reason=error_reason),
            }
            response = render(request, 'error.html', {'context': context})
        return response

    return wrapper