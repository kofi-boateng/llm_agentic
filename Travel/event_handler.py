import os
import requests
# from dotenv import load_dotenv
from langchain.tools import BaseTool
from serpapi import search
from typing import Dict, Any

# Load environment variables from .env file
# dotenv_path = os.path.join('..', '..', '.env')  # Adjusted path for Windows compatibility
# load_dotenv(dotenv_path)

# Access environment variables
# EVENT_API_KEY = os.getenv('SERPAPI_API_KEY')

from google.colab import userdata
EVENT_API_KEY = userdata.get('SERPAPI_API_KEY')

# Check if API key is loaded correctly
if not EVENT_API_KEY:
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

class Events(BaseTool):
    name: str = "events_tool"
    description: str = "Searches for events based on the provided criteria using a event search engine. Provide destination locations to the search."

    def _run(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the event query dictionary.
        :param query: A dictionary containing the query parameters.
        :returns:
            dict: A dictionary containing the search results from the event search engine.
        """
        params = {
            "engine": "google_events",
            "q": query.get('q'),
            "hl": "en",
            "gl": "us",
            "api_key": EVENT_API_KEY
        }

        results = search(params)
        # print(results)
        events_details = [self.get_event_details(event) for event in results.get('events_results', [])]
        return {'Recommended events': query.get('q'), 'Details': events_details}

    def get_event_details(self, dictionary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract event details from the results.
        :param dictionary: A dictionary containing event details.
        :return: A dictionary with extracted event details.
        """
        title = dictionary.get('title', 'N/A')
        start_date = dictionary.get('date', 'N/A')
        address = dictionary.get('address', 'N/A')
        return {'Title': title, 'start_date': start_date, 'address': address}

# if __name__ == "__main__":
#     print("In Event")
#     events_tool = Events()

#     # Define the query parameters as a dictionary
#     query_parameters = {
#         'q': 'New York City',
#         'hl': "en",
#         'g': "us",
#     }

#     # Pass the entire dictionary directly to invoke
#     response = events_tool.invoke({'query': query_parameters})
#     print(response)