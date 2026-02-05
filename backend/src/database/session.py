from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Process the database URL to remove unsupported parameters for asyncpg
if DATABASE_URL and "postgresql" in DATABASE_URL:
    # Remove query parameters that asyncpg doesn't support
    # Use regex to remove problematic parameters
    processed_url = re.sub(r'[?&]sslmode=[^&]*', '', DATABASE_URL)
    processed_url = re.sub(r'[?&]channel_binding=[^&]*', '', processed_url)
    processed_url = re.sub(r'[?&]options=[^&]*', '', processed_url)
    
    # Ensure proper URL formatting after parameter removal
    processed_url = processed_url.replace('?&', '?')
    processed_url = processed_url.replace('&&', '&')
    
    # Convert to asyncpg format
    ASYNC_DATABASE_URL = processed_url.replace("postgresql://", "postgresql+asyncpg://")
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Create async engine
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)