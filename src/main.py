from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.github.router import router as github_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    print(f"[STARTUP] {settings.app_name} v{settings.app_version} started")
    print(f"[INFO] Documentation: http://localhost:8000/docs")
    yield
    # Shutdown
    print(f"[SHUTDOWN] {settings.app_name} stopped")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    REST API to get GitHub user information.
    
    ## Features
    - GitHub personal access token authentication
    - Retrieve complete user information
    - List repositories (public and private)
    - User organizations
    - User pull requests
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(github_router)

