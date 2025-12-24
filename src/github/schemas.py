from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RepositoryInfo(BaseModel):
    """GitHub repository information"""
    name: str = Field(..., description="Repository name")
    full_name: str = Field(..., description="Full name (user/repo)")
    private: bool = Field(..., description="Whether the repository is private or public")
    description: Optional[str] = Field(None, description="Repository description")
    url: str = Field(..., description="Repository URL")
    language: Optional[str] = Field(None, description="Primary programming language")
    stargazers_count: int = Field(..., description="Number of stars")
    forks_count: int = Field(..., description="Number of forks")
    created_at: datetime = Field(..., description="Creation date")


class OrganizationInfo(BaseModel):
    """GitHub organization information"""
    login: str = Field(..., description="Organization username")
    id: int = Field(..., description="Organization ID")
    avatar_url: str = Field(..., description="Avatar URL")
    description: Optional[str] = Field(None, description="Organization description")


class PullRequestInfo(BaseModel):
    """Pull request information"""
    title: str = Field(..., description="Pull request title")
    number: int = Field(..., description="Pull request number")
    state: str = Field(..., description="State (open, closed, merged)")
    repository_url: str = Field(..., description="Repository URL")
    created_at: datetime = Field(..., description="Creation date")


class UserInfo(BaseModel):
    """Basic GitHub user information"""
    login: str = Field(..., description="GitHub username")
    name: Optional[str] = Field(None, description="Full name")
    company: Optional[str] = Field(None, description="Company")
    location: Optional[str] = Field(None, description="Location")
    blog: Optional[str] = Field(None, description="Website/Blog")
    followers: int = Field(..., description="Number of followers")


class SummaryInfo(BaseModel):
    """User statistical summary"""
    public_repos: int = Field(..., description="Number of public repositories")
    public_gists: int = Field(..., description="Number of public gists")
    total_repositories: int = Field(..., description="Total repositories (public + private)")
    total_organizations: int = Field(..., description="Total organizations")
    total_pull_requests: int = Field(..., description="Total pull requests")


class GitHubUserResponse(BaseModel):
    """Complete response with GitHub user information"""
    user: UserInfo = Field(..., description="Basic user information")
    summary: SummaryInfo = Field(..., description="Statistical summary")
    repositories: List[RepositoryInfo] = Field(default_factory=list, description="List of repositories")
    organizations: List[OrganizationInfo] = Field(default_factory=list, description="Organizations")
    pull_requests: List[PullRequestInfo] = Field(default_factory=list, description="User pull requests")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "login": "octocat",
                    "name": "The Octocat",
                    "company": "@github",
                    "location": "San Francisco",
                    "blog": "https://github.blog",
                    "followers": 1000
                },
                "summary": {
                    "public_repos": 8,
                    "public_gists": 8,
                    "total_repositories": 10,
                    "total_organizations": 2,
                    "total_pull_requests": 50
                },
                "repositories": [],
                "organizations": [],
                "pull_requests": []
            }
        }

