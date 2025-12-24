# GitHub User Summary

REST API built with FastAPI to retrieve GitHub user information.

## ✨ Features

- 🚀 REST API with FastAPI
- 🔒 GitHub Personal Access Token authentication
- 📚 Automatic Swagger UI documentation
- 🐳 Dockerized and production-ready
- 🏗️ Modular feature-based architecture
- 🔄 CORS enabled

## 📁 Project Structure

```
github_user_summary/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   └── modules/
│       └── github/
│           ├── controller/
│           ├── schemas/
│           └── services/
├── services/
│   └── github_services/
├── utils/
│   └── error_handler/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🛠️ Prerequisites

- Python >= 3.12
- Docker & Docker Compose (optional)
- GitHub Personal Access Token with the following permissions:
  - `read:user` - Read profile information
  - `repo` - Access repositories and pull requests
  - `read:org` - Read organization membership
  
  → [Create token here](https://github.com/settings/tokens)

## 🚀 Quick Start

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
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 🌐 API Endpoint

### `GET /github/user`
Get authenticated GitHub user information.

**Required Header:**
```
Authorization: Bearer {your_github_token}
```

**Example:**
```bash
curl -H "Authorization: Bearer ghp_your_token" http://localhost:8000/github/user
```

## 📚 Interactive Documentation

Once the server is running, access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Using Swagger UI:**
1. Open http://localhost:8000/docs
2. Click **"Authorize"** button (🔒)
3. Enter your GitHub token (without "Bearer")
4. Click **"Authorize"** → **"Close"**
5. Try endpoints with **"Try it out"** → **"Execute"**

## 🏗️ Architecture

The project uses a **modular feature-based architecture**:

```
HTTP Client
    ↓
Controller (API endpoints)
    ↓
Service (business logic)
    ↓
GitHub Service (API client)
    ↓
GitHub API
```

**Key Components:**
- **Controllers**: Define REST endpoints
- **Services**: Business logic and data processing
- **GitHub Service**: HTTP client for GitHub API with error handling
- **Schemas**: Pydantic models for validation and documentation