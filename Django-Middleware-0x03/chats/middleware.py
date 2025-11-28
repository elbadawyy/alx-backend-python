# chats/middleware.py
from datetime import datetime
import logging

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='requests.log', level=logging.INFO)

class RequestLoggingMiddleware:
    """
    Middleware to log user requests with timestamp, user, and path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Call the next middleware/view
        response = self.get_response(request)
        return response
