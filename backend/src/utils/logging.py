import logging
from fastapi import FastAPI
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def get_logger(name: str = None):
    """Get a logger instance"""
    if name:
        return logging.getLogger(name)
    return logger


def setup_logging(app: FastAPI):
    """Setup logging for the FastAPI application"""
    app.logger = get_logger()
    
    @app.middleware("http")
    async def log_requests(request, call_next):
        app.logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        app.logger.info(f"Response status: {response.status_code}")
        return response