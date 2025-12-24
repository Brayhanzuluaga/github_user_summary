# GitHub User Summary

REST API built with FastAPI to retrieve GitHub user information.

##  Features

-  REST API with FastAPI
-  GitHub Personal Access Token authentication
-  Automatic Swagger UI documentation
-  Dockerized and production-ready
-  Modular feature-based architecture
-  Unit tests with pytest
-  CORS enabled

##  Project Structure

```
github_user_summary/
├── src/
│   ├── github/
│   │   ├── __init__.py
│   │   ├── router.py          # API endpoints
│   │   ├── schemas.py         # Pydantic models
│   │   ├── service.py         # Business logic
│   │   └── client.py          # GitHub API client
│   ├── __init__.py
│   ├── config.py              # Global configuration
│   ├── dependencies.py        # FastAPI dependencies
│   ├── exceptions.py          # Error handlers
│   └── main.py                # FastAPI app
├── tests/
│   ├── __init__.py
│   └── github/
│       ├── __init__.py
│       └── test_service.py    # Service unit tests
├── docker-compose.yml
├── Dockerfile
├── pytest.ini                 # Pytest configuration
├── requirements.txt
└── README.md
```

##  Prerequisites

- Python >= 3.12
- Docker & Docker Compose (optional)
- GitHub Personal Access Token with the following permissions:
  - `read:user` - Read profile information
  - `repo` - Access repositories and pull requests
  - `read:org` - Read organization membership
  
  → [Create token here](https://github.com/settings/tokens)

##  Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Start the service
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

The API will be available at `http://localhost:8000`

### Option 2: Local Python

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## 🧪 Running Tests

### Run All Tests

```bash

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests for a specific module
pytest tests/github/test_service.py
```

### Test Structure

```
tests/
├── github/
│   └── test_service.py    # Tests for GitHubService
└── __init__.py
```

The tests use:
- **pytest** for test framework
- **pytest-asyncio** for async test support
- **unittest.mock** for mocking external dependencies

## 🌐 API Endpoint

### `GET /github/user`
Get authenticated GitHub user information.

**Required Header:**
```
Authorization: Bearer {your_github_token}
```

**Example:**
```bash
curl -H "Authorization: Bearer ghp_your_token" http://localhost:8000/github/user-summary
```

##  Interactive Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Using Swagger UI:**
1. Open http://localhost:8000/docs
2. Click **"Authorize"** button (🔒)
3. Enter your GitHub token (without "Bearer")
4. Click **"Authorize"** → **"Close"**
5. Try endpoints with **"Try it out"** → **"Execute"**

##  Architecture

The project follows **FastAPI best practices** with a **modular feature-based architecture**:

```
HTTP Client
    ↓
Router (API endpoints)
    ↓
Service (business logic)
    ↓
Client (GitHub API communication)
    ↓
GitHub API
```

**Key Components:**
- **Router**: Define REST endpoints and route handling
- **Service**: Business logic and data processing
- **Client**: HTTP client for GitHub API communication
- **Schemas**: Pydantic models for request/response validation
- **Dependencies**: Reusable FastAPI dependencies (auth, etc.)
- **Exceptions**: Centralized error handling