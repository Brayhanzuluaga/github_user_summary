import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.github.service import GitHubService
from src.github.client import GitHubAPIClient


@pytest.fixture
def mock_github_client():
    """Fixture that provides a mocked GitHub client"""
    client = MagicMock(spec=GitHubAPIClient)
    return client


@pytest.fixture
def github_service(mock_github_client):
    """Fixture that provides a GitHubService instance"""
    return GitHubService(github_client=mock_github_client)


class TestProcessRepositories:
    """Tests for _process_repositories"""
    
    def test_process_repositories_success(self, github_service):
        """Should correctly process a list of repositories"""
        repos = [
            {
                "name": "test-repo",
                "full_name": "user/test-repo",
                "private": False,
                "description": "A test repository",
                "html_url": "https://github.com/user/test-repo",
                "language": "Python",
                "stargazers_count": 10,
                "forks_count": 5,
                "created_at": "2023-01-01T00:00:00Z",
            }
        ]
        
        result = github_service._process_repositories(repos)
        
        assert len(result) == 1
        assert result[0]["name"] == "test-repo"
        assert result[0]["full_name"] == "user/test-repo"
        assert result[0]["private"] is False
        assert result[0]["language"] == "Python"
        assert result[0]["stargazers_count"] == 10
    
    def test_process_repositories_empty_list(self, github_service):
        """Should handle an empty list of repositories"""
        repos = []
        
        result = github_service._process_repositories(repos)
        
        assert result == []
    
    def test_process_repositories_missing_fields(self, github_service):
        """Should handle repositories with missing fields"""
        repos = [
            {
                "name": "minimal-repo",
                "full_name": "user/minimal-repo",
            }
        ]
        
        result = github_service._process_repositories(repos)
        
        assert len(result) == 1
        assert result[0]["name"] == "minimal-repo"
        assert result[0]["private"] is False
        assert result[0]["stargazers_count"] == 0


class TestProcessOrganizations:
    """Tests for _process_organizations"""
    
    def test_process_organizations_success(self, github_service):
        """Should correctly process a list of organizations"""
        orgs = [
            {
                "login": "test-org",
                "id": 12345,
                "avatar_url": "https://avatars.githubusercontent.com/u/12345",
                "description": "A test organization",
            }
        ]
        
        result = github_service._process_organizations(orgs)
        
        assert len(result) == 1
        assert result[0]["login"] == "test-org"
        assert result[0]["id"] == 12345
        assert result[0]["description"] == "A test organization"
    
    def test_process_organizations_empty_list(self, github_service):
        """Should handle an empty list of organizations"""
        orgs = []
        
        result = github_service._process_organizations(orgs)
        
        assert result == []


class TestProcessPullRequests:
    """Tests for _process_pull_requests"""
    
    def test_process_pull_requests_success(self, github_service):
        """Should correctly process a list of pull requests"""
        prs = [
            {
                "title": "Test PR",
                "number": 1,
                "state": "open",
                "repository_url": "https://api.github.com/repos/user/repo",
                "created_at": "2023-01-01T00:00:00Z",
            }
        ]
        
        result = github_service._process_pull_requests(prs)
        
        assert len(result) == 1
        assert result[0]["title"] == "Test PR"
        assert result[0]["number"] == 1
        assert result[0]["state"] == "open"
    
    def test_process_pull_requests_empty_list(self, github_service):
        """Should handle an empty list of pull requests"""
        prs = []
        
        result = github_service._process_pull_requests(prs)
        
        assert result == []


class TestGetUserPullRequests:
    """Tests for _get_user_pull_requests"""
    
    @pytest.mark.asyncio
    async def test_get_user_pull_requests_success(self, github_service, mock_github_client):
        """Should successfully get user pull requests"""
        token = "test-token"
        mock_github_client.get_user = AsyncMock(return_value={"login": "testuser"})
        mock_github_client.get_pull_requests = AsyncMock(return_value=[{"title": "PR 1"}])
        
        result = await github_service._get_user_pull_requests(token)
        
        assert len(result) == 1
        assert result[0]["title"] == "PR 1"
        mock_github_client.get_user.assert_called_once_with(token)
        mock_github_client.get_pull_requests.assert_called_once_with(token, "testuser")
    
    @pytest.mark.asyncio
    async def test_get_user_pull_requests_no_login(self, github_service, mock_github_client):
        """Should return empty list if no login exists"""
        token = "test-token"
        mock_github_client.get_user = AsyncMock(return_value={})
        
        result = await github_service._get_user_pull_requests(token)
        
        assert result == []
        mock_github_client.get_user.assert_called_once_with(token)
    
    @pytest.mark.asyncio
    async def test_get_user_pull_requests_exception(self, github_service, mock_github_client):
        """Should return empty list if an exception occurs"""
        token = "test-token"
        mock_github_client.get_user = AsyncMock(side_effect=Exception("API Error"))
        
        result = await github_service._get_user_pull_requests(token)
        
        assert result == []


class TestGetAuthenticatedUser:
    """Tests for get_authenticated_user"""
    
    @pytest.mark.asyncio
    async def test_get_authenticated_user_success(self, github_service, mock_github_client):
        """Should successfully get complete authenticated user information"""
        token = "test-token"
        user_data = {
            "login": "testuser",
            "name": "Test User",
            "company": "Test Company",
            "location": "Test Location",
            "blog": "https://test.com",
            "followers": 100,
            "public_repos": 5,
            "public_gists": 3,
        }
        repos = [{"name": "repo1", "full_name": "testuser/repo1"}]
        orgs = [{"login": "testorg", "id": 123}]
        prs = [{"title": "PR 1", "number": 1}]
        
        mock_github_client.get_user = AsyncMock(return_value=user_data)
        mock_github_client.get_repositories = AsyncMock(return_value=repos)
        mock_github_client.get_organizations = AsyncMock(return_value=orgs)
        mock_github_client.get_pull_requests = AsyncMock(return_value=prs)
        
        result = await github_service.get_authenticated_user(token)
        
        assert result["user"]["login"] == "testuser"
        assert result["user"]["name"] == "Test User"
        assert result["user"]["followers"] == 100
        assert result["summary"]["public_repos"] == 5
        assert result["summary"]["total_repositories"] == 1
        assert result["summary"]["total_organizations"] == 1
        assert result["summary"]["total_pull_requests"] == 1
        assert len(result["repositories"]) == 1
        assert len(result["organizations"]) == 1
        assert len(result["pull_requests"]) == 1
    
    @pytest.mark.asyncio
    async def test_get_authenticated_user_with_partial_errors(
        self, github_service, mock_github_client
    ):
        """Should handle partial errors in secondary calls"""
        token = "test-token"
        user_data = {
            "login": "testuser",
            "name": "Test User",
            "followers": 50,
            "public_repos": 2,
            "public_gists": 1,
        }
        
        mock_github_client.get_user = AsyncMock(return_value=user_data)
        mock_github_client.get_repositories = AsyncMock(side_effect=Exception("Repos error"))
        mock_github_client.get_organizations = AsyncMock(side_effect=Exception("Orgs error"))
        mock_github_client.get_pull_requests = AsyncMock(return_value=[])
        

        result = await github_service.get_authenticated_user(token)
        

        assert result["user"]["login"] == "testuser"
        assert result["repositories"] == []
        assert result["organizations"] == []
        assert result["summary"]["total_repositories"] == 0
        assert result["summary"]["total_organizations"] == 0
    
    @pytest.mark.asyncio
    async def test_get_authenticated_user_user_error(
        self, github_service, mock_github_client
    ):
        """Should propagate error if user data retrieval fails"""
        token = "test-token"
        
        mock_github_client.get_user = AsyncMock(side_effect=Exception("User error"))
        mock_github_client.get_repositories = AsyncMock(return_value=[])
        mock_github_client.get_organizations = AsyncMock(return_value=[])
        mock_github_client.get_pull_requests = AsyncMock(return_value=[])
        
        with pytest.raises(Exception) as exc_info:
            await github_service.get_authenticated_user(token)
        
        assert str(exc_info.value) == "User error"

