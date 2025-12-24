from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import security
from app.modules.github.schemas import GitHubUserResponse, ErrorResponse
from app.modules.github.services import github_service

router = APIRouter(prefix="/github", tags=["GitHub"])


@router.get(
    "/user-summary",
    response_model=GitHubUserResponse,
)
async def get_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> GitHubUserResponse:
    """
    Endpoint to get authenticated GitHub user information.
    
    Args:
        credentials: Bearer credentials with GitHub token
        
    Returns:
        GitHubUserResponse: Detailed user information
    """
    user_data = await github_service.get_authenticated_user(credentials.credentials)
    return GitHubUserResponse(**user_data)
