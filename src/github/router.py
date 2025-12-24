from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.dependencies import get_github_token, get_github_service
from src.github.schemas import GitHubUserResponse
from src.github.service import GitHubService

router = APIRouter(prefix="/github", tags=["GitHub"])


@router.get(
    "/user-summary",
    response_model=GitHubUserResponse,
    summary="Get GitHub user summary",
    description="Get complete authenticated user information including repositories, organizations and pull requests"
)
async def get_user_summary(
    credentials: HTTPAuthorizationCredentials = Depends(get_github_token),
    github_service: GitHubService = Depends(get_github_service)
) -> GitHubUserResponse:
    """
    Endpoint to get complete authenticated GitHub user information.
    
    Args:
        credentials: Bearer credentials with GitHub token
        github_service: GitHub service instance (injected)
        
    Returns:
        GitHubUserResponse: Detailed user information
    """
    user_data = await github_service.get_authenticated_user(credentials.credentials)
    return GitHubUserResponse(**user_data)

