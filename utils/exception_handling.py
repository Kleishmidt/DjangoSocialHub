from functools import wraps
from django.db import OperationalError
from retry import retry


def handle_exception(func):
    @wraps(func)
    @retry(OperationalError, tries=3, delay=1)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            return {'error': f'Failed to execute database operation: {str(e)}'}, 500
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}, 500

    return wrapper
