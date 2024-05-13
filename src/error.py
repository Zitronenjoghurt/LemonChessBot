from src.api.api_controller import ApiResponse

class ApiError(Exception):
    """Exception base class for api-related errors."""

class UnecpectedApiError(ApiError):
    """Raised when the API returned an unexpected response."""
    
    def __init__(self, response: ApiResponse) -> None:
        super().__init__(f"Unexpected API response: [{response.status}] {response.content}")