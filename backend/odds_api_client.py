"""
The Odds API client for fetching real-time sports betting odds
"""

import httpx
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import time

from config import settings

# Configure logger
logger = logging.getLogger(__name__)


class OddsAPIError(Exception):
    """Custom exception for Odds API errors"""
    pass


class RateLimitError(OddsAPIError):
    """Exception for rate limit errors"""
    pass


class OddsAPIClient:
    """Client for interacting with The Odds API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.odds_api_key
        self.base_url = settings.odds_api_base_url
        self.timeout = 30.0
        
        if not self.api_key:
            raise ValueError("ODDS_API_KEY is required")
        
        # Initialize HTTP client
        self.client = httpx.Client(
            timeout=self.timeout,
            headers={"User-Agent": "BetIntel/1.0"}
        )
        
        logger.info(f"Initialized OddsAPIClient with base URL: {self.base_url}")
    
    def __del__(self):
        """Clean up HTTP client"""
        if hasattr(self, 'client'):
            self.client.close()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make HTTP request to The Odds API with error handling
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            API response data
            
        Raises:
            OddsAPIError: For API errors
            RateLimitError: For rate limit errors
        """
        # Add API key to params
        params["apiKey"] = self.api_key
        
        url = f"{self.base_url}{endpoint}"
        
        start_time = time.time()
        
        try:
            logger.info(f"Making request to {url} with params: {params}")
            
            response = self.client.get(url, params=params)
            
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Log response headers for quota tracking
            headers = response.headers
            remaining = headers.get("x-requests-remaining")
            used = headers.get("x-requests-used")
            last = headers.get("x-requests-last")
            
            logger.info(f"Response: {response.status_code}, Time: {response_time:.2f}ms, Quota - Remaining: {remaining}, Used: {used}, Last: {last}")
            
            # Handle rate limiting
            if response.status_code == 429:
                raise RateLimitError("API rate limit exceeded")
            
            # Handle other HTTP errors
            if response.status_code != 200:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(error_msg)
                raise OddsAPIError(error_msg)
            
            # Parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                raise OddsAPIError(f"Invalid JSON response: {e}")
            
            # Add metadata to response
            metadata = {
                "response_time_ms": response_time,
                "requests_remaining": int(remaining) if remaining else None,
                "requests_used": int(used) if used else None,
                "requests_last": int(last) if last else None,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            # Handle both dict and list responses
            if isinstance(data, dict):
                data["_metadata"] = metadata
            else:
                # For list responses, wrap in a dict with metadata
                data = {
                    "data": data,
                    "_metadata": metadata
                }
            
            return data
            
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            raise OddsAPIError(f"Request failed: {e}")
    
    def get_sports(self, all_sports: bool = False) -> List[Dict[str, Any]]:
        """
        Get list of available sports
        
        Args:
            all_sports: If True, returns all sports (in and out of season)
            
        Returns:
            List of sports data
        """
        params = {}
        if all_sports:
            params["all"] = "true"
        
        data = self._make_request("/sports", params)
        return data
    
    def get_odds(self, 
                 sport: str,
                 regions: str = "us",
                 markets: str = "h2h",
                 odds_format: str = "american",
                 date_format: str = "iso") -> List[Dict[str, Any]]:
        """
        Get current odds for a sport
        
        Args:
            sport: Sport key (e.g., 'basketball_nba')
            regions: Comma-separated regions (us, uk, eu, au)
            markets: Comma-separated markets (h2h, spreads, totals)
            odds_format: Odds format (american, decimal)
            date_format: Date format (iso, unix)
            
        Returns:
            List of events with odds data
        """
        params = {
            "regions": regions,
            "markets": markets,
            "oddsFormat": odds_format,
            "dateFormat": date_format
        }
        
        endpoint = f"/sports/{sport}/odds"
        data = self._make_request(endpoint, params)
        
        return data
    
    def get_events(self, sport: str, date_format: str = "iso") -> List[Dict[str, Any]]:
        """
        Get upcoming events for a sport (without odds)
        
        Args:
            sport: Sport key
            date_format: Date format (iso, unix)
            
        Returns:
            List of upcoming events
        """
        params = {
            "dateFormat": date_format
        }
        
        endpoint = f"/sports/{sport}/events"
        data = self._make_request(endpoint, params)
        
        return data
    
    def get_scores(self, sport: str, days_from: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get scores for completed and live games
        
        Args:
            sport: Sport key
            days_from: Number of days in the past to include completed games
            
        Returns:
            List of games with scores
        """
        params = {}
        if days_from:
            params["daysFrom"] = str(days_from)
        
        endpoint = f"/sports/{sport}/scores"
        data = self._make_request(endpoint, params)
        
        return data


def get_odds_client() -> OddsAPIClient:
    """Get configured odds API client"""
    return OddsAPIClient()


# Example usage and testing
if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO)
    
    try:
        client = get_odds_client()
        
        # Test getting sports
        sports = client.get_sports()
        print(f"Available sports: {len(sports)}")
        
        # Test getting MLB odds
        mlb_odds = client.get_odds(
            sport="baseball_mlb",
            regions="us",
            markets="h2h,spreads,totals",
            odds_format="american"
        )
        print(f"MLB events with odds: {len(mlb_odds)}")
        
        if mlb_odds:
            print(f"Sample event: {mlb_odds[0]['home_team']} vs {mlb_odds[0]['away_team']}")
        
    except Exception as e:
        print(f"Error: {e}") 