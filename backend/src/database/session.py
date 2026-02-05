from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create async engine - replace psycopg2 with asyncpg for async operations
if DATABASE_URL and "postgresql" in DATABASE_URL:
    # Replace postgresql:// with postgresql+asyncpg:// for async operations
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    # Handle Neon-specific connection parameters that need to be adjusted for asyncpg
    # Remove channel_binding parameter which asyncpg doesn't support
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("&channel_binding=require", "")

    # Remove sslmode parameter which causes issues with asyncpg
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("sslmode=require&", "")
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("&sslmode=require", "")
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("?sslmode=require", "?")

    # Ensure the URL doesn't have double ?? after parameter removal
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("??", "?")

else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Create async engine
engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)