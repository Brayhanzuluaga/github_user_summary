from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.modules.github.controller import router as github_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    print(f"🚀 {settings.app_name} v{settings.app_version} started")
    print(f"📚 Documentation: http://localhost:8000/docs")
    yield
    # Shutdown
    print(f"👋 {settings.app_name} stopped")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    REST API to get GitHub user information.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(github_router)
