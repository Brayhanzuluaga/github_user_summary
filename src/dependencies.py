from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from src.config import Settings, get_settings
from src.github.client import GitHubAPIClient
from src.github.service import GitHubService


security = HTTPBearer(
    scheme_name="GitHub Token",
    description="Enter your GitHub personal access token"
)


def get_github_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> HTTPAuthorizationCredentials:
    return credentials


def get_github_client(
    settings: Settings = Depends(get_settings)
) -> GitHubAPIClient:
    """Dependency to get GitHub API client instance"""
    return GitHubAPIClient(settings=settings)


def get_github_service(
    github_client: GitHubAPIClient = Depends(get_github_client)
) -> GitHubService:
    """Dependency to get GitHub service instance"""
    return GitHubService(github_client=github_client)

