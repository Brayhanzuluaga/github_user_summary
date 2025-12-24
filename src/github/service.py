from typing import Dict, Any
import asyncio

from src.github.client import GitHubAPIClient


class GitHubService:
    """Service with business logic for GitHub operations"""
    
    def __init__(self, github_client: GitHubAPIClient):
        self.github_client = github_client
    
    async def get_authenticated_user(self, token: str) -> Dict[str, Any]:
        """
        Gets and processes complete authenticated user information.
        
        Retrieves:
        - Basic user information
        - Repositories (public and private)
        - Organizations
        - Pull Requests
        
        Args:
            token: GitHub personal access token
            
        Returns:
            Dict with complete processed user information in the requested structure
        """
        user_data, repositories, organizations, pull_requests = await asyncio.gather(
            self.github_client.get_user(token),
            self.github_client.get_repositories(token),
            self.github_client.get_organizations(token),
            self._get_user_pull_requests(token),
            return_exceptions=True
        )
        
        if isinstance(user_data, Exception):
            raise user_data
        
        if isinstance(repositories, Exception):
            repositories = []
        if isinstance(organizations, Exception):
            organizations = []
        if isinstance(pull_requests, Exception):
            pull_requests = []
        
        processed_repos = self._process_repositories(repositories)
        processed_orgs = self._process_organizations(organizations)
        processed_prs = self._process_pull_requests(pull_requests)
        
        return {
            "user": {
                "login": user_data.get("login"),
                "name": user_data.get("name"),
                "company": user_data.get("company"),
                "location": user_data.get("location"),
                "blog": user_data.get("blog"),
                "followers": user_data.get("followers", 0),
            },
            "summary": {
                "public_repos": user_data.get("public_repos", 0),
                "public_gists": user_data.get("public_gists", 0),
                "total_repositories": len(repositories),
                "total_organizations": len(organizations),
                "total_pull_requests": len(pull_requests),
            },
            "repositories": processed_repos,
            "organizations": processed_orgs,
            "pull_requests": processed_prs,
        }
    
    async def _get_user_pull_requests(self, token: str) -> list:
        """Gets user pull requests safely"""
        try:
            user_data = await self.github_client.get_user(token)
            username = user_data.get("login")
            if username:
                return await self.github_client.get_pull_requests(token, username)
            return []
        except Exception:
            # If we can't get user data or PRs, return empty list
            return []
    
    def _process_repositories(self, repos: list) -> list:
        """Processes and formats repository list"""
        return [
            {
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "private": repo.get("private", False),
                "description": repo.get("description"),
                "url": repo.get("html_url"),
                "language": repo.get("language"),
                "stargazers_count": repo.get("stargazers_count", 0),
                "forks_count": repo.get("forks_count", 0),
                "created_at": repo.get("created_at"),
            }
            for repo in repos
        ]
    
    def _process_organizations(self, orgs: list) -> list:
        """Processes and formats organization list"""
        return [
            {
                "login": org.get("login"),
                "id": org.get("id"),
                "avatar_url": org.get("avatar_url"),
                "description": org.get("description"),
            }
            for org in orgs
        ]
    
    def _process_pull_requests(self, prs: list) -> list:
        """Processes and formats pull request list"""
        return [
            {
                "title": pr.get("title"),
                "number": pr.get("number"),
                "state": pr.get("state"),
                "repository_url": pr.get("repository_url"),
                "created_at": pr.get("created_at"),
            }
            for pr in prs
        ]

