import logging
import logging.handlers
import json
import re
from django.utils.timezone import now
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpRequest, HttpResponse

# Set up a logger named "api-requests"
logger = logging.getLogger("api-requests")
logger.setLevel(20)  # Set log level to INFO (20)

# Create a rotating file handler:
# Logs will be saved in 'requests.log'
# Each file max size: 10 MB
# Keep up to 5 backup log files
file_handler = logging.handlers.RotatingFileHandler(
    'requests.log', 
    maxBytes=10 * 1024 * 1024, 
    backupCount=5
)

# Define log message format to include timestamp, user, HTTP method, path, and status code
formatter = logging.Formatter(
    '%(asctime)s - User: %(user)s - Method: %(method)s - Path: %(path)s - Status: %(status)s'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware to log requests made to /api/chats/ endpoints with user context.

    It tracks API usage for debugging and auditing by logging:
    - Timestamp of request
    - Authenticated user (from JWT)
    - HTTP method (GET, POST, etc.)
    - Request path
    - Response status code
    - Sanitized request payload (to protect sensitive data)

    It focuses on monitoring chat-related API endpoints like
    /api/chats/users/ and /api/chats/conversations/.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response (callable): The next middleware or view in the request chain.

        Sets up:
        - JWTAuthentication instance to decode JWT tokens.
        - A compiled regex pattern to match URLs starting with '/api/chats/'.
        """
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()
        self.api_pattern = re.compile(r'^/api/chats/')  # Regex to filter relevant API endpoints
        
        
    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Process the incoming request and log relevant details if it matches the /api/chats/ path.

        Steps:
        1. Skip logging if the request path does not start with /api/chats/.
        2. Attempt to extract the username from the JWT token in the Authorization header.
        3. For POST, PUT, PATCH requests, read and sanitize the request payload.
        4. Pass the request to the next middleware/view and capture the response.
        5. Log the collected information: user, method, path, status, and sanitized payload.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The response from the next middleware or view.
        """
        # If the request path does not match /api/chats/, skip logging and return response directly
        if not self.api_pattern.match(request.path):
            return self.get_response(request)
        
        # Default user is 'Anonymous' if authentication fails or is missing
        user: str = 'Anonymous'
        try:
            # Extract the Bearer token from the Authorization header
            token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
            # Validate the token
            validated_token = self.jwt_auth.get_validated_token(token)
            # Retrieve the user object linked to the token
            user_object = self.jwt_auth.get_user(validated_token)
            user = user_object.username  # Extract username
        except Exception:
            # If any error occurs (e.g., token missing/invalid), keep user as 'Anonymous'
            pass
        
        # Prepare to capture and sanitize the request payload if applicable
        payload: str = 'N/A'  # Default when no payload is expected
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                # Decode the raw request body to a string
                body = request.body.decode('utf-8')
                # Parse JSON body into a dict
                payload_dict = json.loads(body) if body else {}
                # Sanitize sensitive fields before logging
                payload = json.dumps(self._sanitize_payload(payload_dict))
            except (UnicodeDecodeError, json.JSONDecodeError):
                # If decoding or parsing fails, mark payload as invalid
                payload = 'Invalid payload'
        
        # Call the next middleware or view, get the response
        response = self.get_response(request)
        
        # Log all relevant info with the logger configured earlier
        logger.info(
            '',  # Message is empty because info is passed via 'extra' dict
            extra={
                'user': user,
                'method': request.method,
                'path': request.path,
                'status': response.status_code,
                'payload': payload
            }
        )
        
        return response


    def _sanitize_payload(self, payload: dict) -> dict:
        """
        Sanitize sensitive information in the payload to avoid logging secrets.

        Args:
            payload (dict): The original JSON payload.

        Returns:
            dict: Payload with sensitive fields masked with '****'.
        """
        sensitive_fields = {'password', 'token', 'access', 'refresh'}
        return {
            k: '****' if k in sensitive_fields else v
            for k, v in payload.items()
        }
