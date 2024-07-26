import os
import requests
from dotenv import load_dotenv
from langchain.tools import BaseTool
from serpapi import search
from typing import Dict, Any

# Load environment variables from .env file
dotenv_path = os.path.join('..', '..', '.env')  # Adjusted path for Windows compatibility
load_dotenv(dotenv_path)

# Access environment variables
HOTEL_API_KEY = os.getenv('SERPAPI_API_KEY')

# Check if API key is loaded correctly
if not HOTEL_API_KEY:
    raise ValueError("API key not found. Please check your .env file.")

# def search(params: Dict) -> Dict:
#     try:
#         response = requests.get('https://serpapi.com/search.json', params=params)
#         response.raise_for_status()  # Raises HTTPError for bad responses
#         return response.json()  # Return JSON response if successful
#     except requests.exceptions.HTTPError as e:
#         print(f"HTTPError: {e}")
#         raise
#     except requests.exceptions.RequestException as e:
#         print(f"RequestException: {e}")
#         raise

class Hotels(BaseTool):
    name: str = "hotels_tool"
    description: str = "Searches for hotels based on the provided criteria using a hotel search engine. Provide destination locations to the search."

    def _run(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the hotel query dictionary.
        :param query: A dictionary containing the query parameters.
        :returns:
            dict: A dictionary containing the search results from the hotel search engine.
        """
        params = {
            "engine": "google_hotels",
            "q": query.get('q'),
            "check_in_date": query.get('check_in_date'),
            "check_out_date": query.get('check_out_date'),
            "currency": query.get('currency'),
            "hl": "en",
            "adults": 2 if query.get('return_date') is None else 1,
            "api_key": HOTEL_API_KEY
        }

        results = search(params)
        # print(results)
        hotels_details = [self.get_hotel_details(hotel) for hotel in results.get('brands', [])]
        return {'Destination': query.get('q'), 'hotel_details': hotels_details}

    def get_hotel_details(self, dictionary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract hotel details from the results.
        :param dictionary: A dictionary containing hotel details.
        :return: A dictionary with extracted hotel details.
        """
        name = dictionary.get('name', 'N/A')
        rate = dictionary.get('rate_per_night', 'N/A')
        overall_rating = dictionary.get('overall_rating', 'N/A')
        return {'property_name': name, 'rate_per_night': rate, 'rating': overall_rating}

if __name__ == "__main__":
    print("In hotel")
    hotels_tool = Hotels()

    # Define the query parameters as a dictionary
    query_parameters = {
        'q': 'New York City',
        'check_in_date': '2024-07-27',
        'check_out_date': '2024-07-30',
        'currency': 'USD'
    }

    # Pass the entire dictionary directly to invoke
    response = hotels_tool.invoke({'query': query_parameters})
    print(response)
