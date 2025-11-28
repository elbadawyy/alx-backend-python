# chats/middleware.py
from datetime import datetime
import logging

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Django passes this automatically

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)  # continue to next middleware/view
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

