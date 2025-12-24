import httpx
from typing import Dict, Any, Optional
from fastapi import HTTPException


class HTTPErrorHandler:
    """Helper class for centralized and reusable HTTP error handling"""
    
    DEFAULT_ERROR_MESSAGES: Dict[int, str] = {
        400: "Invalid request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Resource not found",
        422: "Invalid input data",
        429: "Too many requests",
        500: "Internal server error",
        502: "Bad gateway",
        503: "Service unavailable",
        504: "Gateway timeout",
    }
    
    def __init__(self, custom_messages: Optional[Dict[int, str]] = None):
        self.error_messages = {**self.DEFAULT_ERROR_MESSAGES}
        if custom_messages:
            self.error_messages.update(custom_messages)
    
    def handle_response(
        self, 
        response: httpx.Response,
        success_status: int = 200
    ) -> Dict[str, Any]:
        if response.status_code == success_status:
            return response.json()
        
        detail = self.error_messages.get(
            response.status_code,
            f"HTTP Error {response.status_code}: {response.text}"
        )
        
        raise HTTPException(status_code=response.status_code, detail=detail)
    
    def handle_timeout(self) -> None:
        raise HTTPException(
            status_code=504,
            detail="Timeout connecting to external service"
        )
    
    def handle_connection_error(self, error: Exception) -> None:
        raise HTTPException(
            status_code=503,
            detail=f"Connection error: {str(error)}"
        )
