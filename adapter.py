import os
import requests
from typing import Optional, List
import logging
import random
from pydantic import BaseModel, Field, HttpUrl

logger = logging.getLogger(__name__)

class GiphyImage(BaseModel):
    """Model representing a single image variant from Giphy."""
    width: int
    height: int
    url: HttpUrl

class GiphyGif(BaseModel):
    """Pydantic model representing a Giphy GIF with essential attributes."""
    id: str
    url: HttpUrl
    title: str
    rating: str
    width: int
    height: int
    content_url: HttpUrl = Field(alias="original_url")
    
    class Config:
        allow_population_by_field_name = True

class GiphySearchResponse(BaseModel):
    """Model representing the response from Giphy search API."""
    data: List[dict]
    pagination: dict
    meta: dict

class GiphyGetResponse(BaseModel):
    """Model representing the response from Giphy get-by-id API."""
    data: dict
    meta: dict

class GiphyAdapter:
    """Adapter for interacting with the Giphy API using Pydantic models."""
    
    BASE_URL = "https://api.giphy.com/v1/gifs"
    
    def __init__(self, api_key: str = None):
        """Initialize the Giphy adapter with API key."""
        self.api_key = api_key or os.environ.get("GIPHY_API_KEY")
        if not self.api_key:
            raise ValueError("Giphy API key is required")
            
    def search_gif(self, query: str, limit: int = 10, rating: str = "g") -> Optional[GiphyGif]:
        """
        Search for a GIF based on the provided text query.
        
        Args:
            query: Text to search for
            limit: Maximum number of results to return
            rating: Content rating (g, pg, pg-13, r)
            
        Returns:
            A randomly selected GiphyGif object from the results, or None if no results
        """
        try:
            endpoint = f"{self.BASE_URL}/search"
            params = {
                "api_key": self.api_key,
                "q": query,
                "limit": limit,
                "rating": rating,
            }
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            search_response = GiphySearchResponse(**response.json())
            gifs = search_response.data
            
            if not gifs:
                logger.info(f"No GIFs found for query: {query}")
                return None
                
            # Select a random GIF from the results for variety
            selected = random.choice(gifs)
            
            # Map the response to our model
            return GiphyGif(
                id=selected["id"],
                url=selected["url"],
                title=selected["title"],
                rating=selected["rating"],
                width=selected["images"]["original"]["width"],
                height=selected["images"]["original"]["height"],
                original_url=selected["images"]["original"]["url"]
            )
            
        except requests.RequestException as e:
            logger.error(f"Error fetching GIF from Giphy: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"Error parsing Giphy response: {str(e)}")
            return None
    
    def get_gif_by_id(self, gif_id: str) -> Optional[GiphyGif]:
        """
        Get a specific GIF by its ID.
        
        Args:
            gif_id: The Giphy ID of the GIF
            
        Returns:
            A GiphyGif object or None if not found
        """
        try:
            endpoint = f"{self.BASE_URL}/{gif_id}"
            params = {
                "api_key": self.api_key
            }
            
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            
            get_response = GiphyGetResponse(**response.json())
            gif_data = get_response.data
            
            if not gif_data:
                logger.info(f"No GIF found with ID: {gif_id}")
                return None
                
            return GiphyGif(
                id=gif_data["id"],
                url=gif_data["url"],
                title=gif_data["title"],
                rating=gif_data["rating"],
                width=gif_data["images"]["original"]["width"],
                height=gif_data["images"]["original"]["height"],
                original_url=gif_data["images"]["original"]["url"]
            )
            
        except requests.RequestException as e:
            logger.error(f"Error fetching GIF from Giphy: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"Error parsing Giphy response: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    adapter = GiphyAdapter()
    gif = adapter.search_gif("excited")
    if gif:
        print(f"Found GIF: {gif.title}")
        print(f"URL: {gif.content_url}")