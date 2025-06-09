import logging
import logging.handlers
import json
import re
from django.utils.timezone import now
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from typing import Callable
from datetime import datetime



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
        self.api_pattern = re.compile(r'^/api/(chats/|users/)')  # Regex to filter relevant API endpoints
        
        
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


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response: Callable) -> None:
        # get_response is the next middleware or view; it will be called if access is allowed
        self.get_response = get_response

        # This regular expression is used to match only the specific API path we want to restrict
        # It ensures that only requests to /api/chats/conversations/messages are affected
        self.api_patterns = re.compile(r'^/api/chats/conversations/')

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Check if the current request's path matches the restricted API endpoint
        if not self.api_patterns.match(request.path):
            # If not matching, bypass the restriction and pass request to the next layer
            return self.get_response(request)

        # Get the current hour (0 to 23) in Coordinated Universal Time (UTC)
        # For example, 18 means 6 PM UTC, 21 means 9 PM UTC
        current_hour = datetime.utcnow().hour

        # Define the allowed window as between 18 (6 PM) and 21 (9 PM), UTC time
        # The condition checks if the current hour is *outside* that range
        if not (00 <= current_hour < 21):
            # If the current time is not within the allowed range, block access
            # Return a 403 Forbidden response with a JSON body explaining the restriction
            return HttpResponseForbidden(
                json.dumps({
                    "error": "Access restricted outside 6 PM to 9 PM (UTC)"
                }),
                content_type='application/json'
            )

        # If the request passed the time check, continue processing normally
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    """
    Middleware to filter out offensive language in chat messages.

    This middleware targets POST requests to conversation message endpoints
    and scans the message content for predefined offensive words. If such
    language is detected, it blocks the request and returns a 403 Forbidden 
    response with an appropriate error message.

    Targeted Endpoint Pattern:
    - /api/chats/conversations/<uuid>/messages/

    Offensive terms are defined via a case-insensitive regular expression.
    """

    def __init__(self, get_response: Callable):
        """
        Initializes the middleware.

        Args:
            get_response (Callable): The next layer in the middleware stack.

        Sets:
            - api_patterns: Regex pattern to match valid message POST endpoints.
            - offensive_words: Regex to match specific offensive terms in a message.
        """
        self.get_response = get_response

        # This regex matches valid POST targets like:
        # /api/chats/conversations/123e4567-e89b-12d3-a456-426614174000/messages/
        self.api_patterns = re.compile(r'^/api/chats/conversations/messages/$')

        # Offensive words pattern (case-insensitive)
        self.offensive_words = re.compile(
            r'\b(?:buddy|idiot|dude|nigga|stupid)\b',
            re.IGNORECASE
        )

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        Intercepts and evaluates POST requests to conversation message endpoints.

        Steps:
        1. Only evaluate POST requests that match the conversation message path.
        2. Attempt to decode and parse the request body as JSON.
        3. Search for offensive language in the 'message' field of the payload.
        4. If found, return 403 Forbidden with an error; else allow normal flow.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: Either a forbidden response or the original view response.
        """
        # Skip non-POST requests or paths that don't match the target pattern
        if request.method != 'POST' or not self.api_patterns.match(request.path):
            return self.get_response(request)

        try:
            # Decode the raw body into a string (assuming UTF-8)
            body = request.body.decode('utf-8')

            # Parse JSON payload into a Python dictionary
            payload = json.loads(body) if body else {}

            # Extract message content, default to empty string if not found
            message = payload.get("message_body", "") if isinstance(payload, dict) else ""

            # If the message contains offensive language, block the request
            if self.offensive_words.search(message):
                return HttpResponseForbidden(
                    json.dumps({
                        "Error": "Your message contains offensive language. Please edit !."
                    }),
                    content_type="application/json"
                )

        except Exception as e:
            # If decoding or parsing fails, treat the message as invalid
            return HttpResponseForbidden(
                json.dumps({
                    "Error": "Invalid message format or payload."
                }),
                content_type="application/json"
            )

        # If all checks pass, continue to the next middleware/view
        return self.get_response(request)

        
