from fastapi.security import HTTPBearer

security = HTTPBearer(
    scheme_name="GitHub Token",
    description="Enter your personal GitHub access token"
)

