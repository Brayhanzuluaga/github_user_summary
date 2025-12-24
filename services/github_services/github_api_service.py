import httpx
from typing import Dict, Any, List

from app.core.config import settings
from utils.error_handler import HTTPErrorHandler


class GitHubAPIClient:
    """Client for communicating with GitHub API"""
    
    def __init__(self):
        self.base_url = settings.github_api_base_url
        self.api_version = settings.github_api_version
        self.error_handler = HTTPErrorHandler()
    
    def _get_headers(self, token: str) -> Dict[str, str]:
        """Generates common headers for GitHub requests"""
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": self.api_version
        }
    
    async def get_user(self, token: str) -> Dict[str, Any]:
        """
        Gets authenticated user information from GitHub API.
        
        Args:
            token: GitHub personal access token
            
        Returns:
            Dict with user information from GitHub
            
        Raises:
            HTTPException: If there's an error in the request
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/user",
                    headers=self._get_headers(token),
                    timeout=10.0
                )
                return self.error_handler.handle_response(response)
                
        except httpx.TimeoutException:
            self.error_handler.handle_timeout()
        except httpx.RequestError as e:
            self.error_handler.handle_connection_error(e)
    
    async def get_repositories(self, token: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Gets authenticated user repositories (public and private).
        
        Args:
            token: GitHub personal access token
            per_page: Number of repositories per page (max 100)
            
        Returns:
            List of repositories
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/user/repos",
                    headers=self._get_headers(token),
                    params={"per_page": per_page, "sort": "updated", "type": "all"},
                    timeout=15.0
                )
                return self.error_handler.handle_response(response)
                
        except httpx.TimeoutException:
            self.error_handler.handle_timeout()
        except httpx.RequestError as e:
            self.error_handler.handle_connection_error(e)
    
    async def get_organizations(self, token: str) -> List[Dict[str, Any]]:
        """
        Gets organizations the user belongs to.
        
        Args:
            token: GitHub personal access token
            
        Returns:
            List of organizations
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/user/orgs",
                    headers=self._get_headers(token),
                    timeout=10.0
                )
                return self.error_handler.handle_response(response)
                
        except httpx.TimeoutException:
            self.error_handler.handle_timeout()
        except httpx.RequestError as e:
            self.error_handler.handle_connection_error(e)
    
    async def get_pull_requests(self, token: str, username: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Gets pull requests created by the user.
        
        Args:
            token: GitHub personal access token
            username: User username
            per_page: Number of PRs per page (max 100)
            
        Returns:
            List of pull requests
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/search/issues",
                    headers=self._get_headers(token),
                    params={
                        "q": f"author:{username} type:pr",
                        "per_page": per_page,
                        "sort": "updated"
                    },
                    timeout=15.0
                )
                result = self.error_handler.handle_response(response)
                return result.get("items", [])
                
        except httpx.TimeoutException:
            self.error_handler.handle_timeout()
        except httpx.RequestError as e:
            self.error_handler.handle_connection_error(e)
