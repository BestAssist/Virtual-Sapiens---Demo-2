import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware that logs request path, execution time, and status code.
    """

    def __init__(self, app: ASGIApp):
        """
        Initialize the logging middleware.

        Args:
            app: The ASGI application to wrap
        """
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Record start time
        start_time = time.time()
        
        # Get request path
        path = request.url.path
        
        # Process the request
        response = await call_next(request)
        
        # Calculate execution time
        execution_time = (time.time() - start_time) * 1000  # in milliseconds
        
        # Get status code
        status_code = response.status_code
        
        # Log the information
        logger.info(
            f"Path: {path} | "
            f"Execution Time: {execution_time:.4f}s | "
            f"Status Code: {status_code}"
        )
        
        return response

