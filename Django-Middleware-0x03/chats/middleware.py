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
    
class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to chats outside 6AM - 9PM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict chat endpoints
        if request.path.startswith("/api/conversations/"):
            now = datetime.now().time()
            start_time = datetime.strptime("06:00", "%H:%M").time()
            end_time = datetime.strptime("21:00", "%H:%M").time()

            if not (start_time <= now <= end_time):
                return HttpResponseForbidden("Chat access is only allowed between 6AM and 9PM")

        # Continue to next middleware/view
        response = self.get_response(request)
        return response


