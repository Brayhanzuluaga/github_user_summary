import httpx
from typing import Dict, Any
from fastapi import HTTPException


DEFAULT_ERROR_MESSAGES: Dict[int, str] = {
    400: "Invalid request",
    401: "Unauthorized - Invalid or expired GitHub token",
    403: "Forbidden - Insufficient token permissions",
    404: "Resource not found",
    422: "Invalid input data",
    429: "Too many requests - Rate limit exceeded",
    500: "Internal server error",
    502: "Bad gateway",
    503: "Service unavailable",
    504: "Gateway timeout",
}


def handle_github_response(response: httpx.Response, success_status: int = 200) -> Dict[str, Any]:
    if response.status_code == success_status:
        return response.json()
    
    detail = DEFAULT_ERROR_MESSAGES.get(
        response.status_code,
        f"HTTP Error {response.status_code}: {response.text}"
    )
    
    raise HTTPException(status_code=response.status_code, detail=detail)


def handle_timeout() -> None:
    raise HTTPException(
        status_code=504,
        detail="Timeout connecting to external service"
    )


def handle_connection_error(error: Exception) -> None:
    raise HTTPException(
        status_code=503,
        detail=f"Connection error: {str(error)}"
    )

