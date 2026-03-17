from rest_framework.views import exception_handler
import logging
logger = logging.getLogger(__name__)

def custom_exception_handler(exception, context):
    logger.error(f"API error: {exception}")
    response = exception_handler(exception, context)

    if response is not None:
        response.data = {
            "error": True,
            "status_code": response.status_code,
            "message": response.data
        }

    return response