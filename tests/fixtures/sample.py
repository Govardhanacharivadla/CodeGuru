"""Sample async function for testing."""

import asyncio
import httpx


async def fetch_user_data(user_id: int, api_url: str = "https://api.example.com") -> dict:
    """
    Fetch user data from an API asynchronously.
    
    This function demonstrates async/await patterns and HTTP requests.
    
    Args:
        user_id: The ID of the user to fetch
        api_url: Base URL of the API
    
    Returns:
        dict containing user data
    
    Raises:
        httpx.HTTPError: If the API request fails
    """
    # Create async HTTP client
    async with httpx.AsyncClient() as client:
        # Construct endpoint URL
        endpoint = f"{api_url}/users/{user_id}"
        
        try:
            # Make async HTTP GET request
            response = await client.get(endpoint, timeout=10.0)
            
            # Raise exception for bad status codes
            response.raise_for_status()
            
            # Parse JSON response
            user_data = response.json()
            
            # Transform data
            processed_data = {
                "id": user_data.get("id"),
                "name": user_data.get("name"),
                "email": user_data.get("email"),
                "created_at": user_data.get("created_at")
            }
            
            return processed_data
            
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise


async def fetch_multiple_users(user_ids: list[int]) -> list[dict]:
    """
    Fetch data for multiple users concurrently.
    
    Demonstrates concurrent async operations using asyncio.gather.
    """
    # Create tasks for all user fetches
    tasks = [fetch_user_data(user_id) for user_id in user_ids]
    
    # Run all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out failed requests
    successful_results = [
        result for result in results 
        if not isinstance(result, Exception)
    ]
    
    return successful_results


def sync_fetch_user(user_id: int) -> dict:
    """
    Synchronous version for comparison.
    
    This blocks the entire thread while waiting for the response.
    """
    endpoint = f"https://api.example.com/users/{user_id}"
    
    # Blocking HTTP request
    response = httpx.get(endpoint)
    return response.json()


class UserManager:
    """Manages user data with async methods."""
    
    def __init__(self, api_url: str):
        """Initialize user manager."""
        self.api_url = api_url
        self.cache = {}
    
    async def get_user(self, user_id: int, use_cache: bool = True) -> dict:
        """Get user data with optional caching."""
        # Check cache first
        if use_cache and user_id in self.cache:
            return self.cache[user_id]
        
        # Fetch from API
        user_data = await fetch_user_data(user_id, self.api_url)
        
        # Store in cache
        if use_cache:
            self.cache[user_id] = user_data
        
        return user_data
    
    async def update_user(self, user_id: int, updates: dict) -> dict:
        """Update user data."""
        async with httpx.AsyncClient() as client:
            endpoint = f"{self.api_url}/users/{user_id}"
            response = await client.patch(endpoint, json=updates)
            response.raise_for_status()
            
            # Invalidate cache
            if user_id in self.cache:
                del self.cache[user_id]
            
            return response.json()


if __name__ == "__main__":
    # Example usage
    async def main():
        # Fetch single user
        user = await fetch_user_data(123)
        print(f"User: {user}")
        
        # Fetch multiple users concurrently
        users = await fetch_multiple_users([1, 2, 3, 4, 5])
        print(f"Fetched {len(users)} users")
    
    asyncio.run(main())
