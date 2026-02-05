from fastapi import FastAPI
from src.api.tasks import router as tasks_router
from contextlib import asynccontextmanager
from src.database.session import engine
from sqlmodel import SQLModel
from src.utils.exception_handlers import add_exception_handlers
from src.utils.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # Cleanup on shutdown


app = FastAPI(
    title="Todo API",
    description="Backend API for the Phase II Todo app",
    version="1.0.0",
    lifespan=lifespan
)

# Setup logging
setup_logging(app)

# Add exception handlers
add_exception_handlers(app)

# Include routers
app.include_router(tasks_router, prefix="/api/{user_id}", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}