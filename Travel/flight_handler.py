import os
import requests
from dotenv import load_dotenv
from langchain.tools import BaseTool
# from serpapi import search
from typing import Dict

from google.colab import userdata
FLIGHT_API_KEY = userdata.get('SERPAPI_API_KEY')

# Load environment variables from .env file
# dotenv_path = os.path.join('../..', '.env')

# load_dotenv(dotenv_path)

# Access environment variables
# FLIGHT_API_KEY = os.getenv('SERPAPI_API_KEY')

# print(f'Key: {FLIGHT_API_KEY}')

# Check if API key is loaded correctly
if not FLIGHT_API_KEY:
    raise ValueError("API key not found. Please check your .env file.")

def search(params: Dict) -> Dict:
    try:
        response = requests.get('https://serpapi.com/search', params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()  # Return JSON response if successful
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        raise

class Flights(BaseTool):
    name: str = "flights_tool"
    description: str = "Searches for flights based on the provided criteria using a flight search engine. Provide Google Flights IDs for the locations."

    def _run(self, query: Dict) -> Dict:
        """
        Process the flight query dictionary.
        :param query: A dictionary containing the query parameters.
        :returns:
            dict: A dictionary containing the search results from the flight search engine.
        """
        params = {
            "engine": "google_flights",
            "departure_id": query.get('origin'),
            "arrival_id": query.get('destination'),
            "outbound_date": query.get('departure_date'),
            "return_date": query.get('return_date'),
            "currency": query.get('currency'),
            "hl": "en",
            "type": 2 if query.get('return_date') is None else 1,
            "api_key": FLIGHT_API_KEY
        }

        results = search(params)
        flights_details = [self.get_flight_details(flight) for flight in results.get('other_flights', [])]
        return {'Departure': query.get('origin'), 'Arrival': query.get('destination'), 'flight_details': flights_details}

    def get_flight_details(self, dictionary: Dict) -> Dict:
        """
        Extract flight details from the results.
        :param dictionary: A dictionary containing flight details.
        :return: A dictionary with extracted flight details.
        """
        airlines = [flight['airline'] for flight in dictionary.get('flights', [])]
        layover_stations = dictionary.get('layovers', 'NA')
        total_duration = dictionary.get('total_duration', 'Not Provided')
        price = dictionary.get('price', 'Not Provided')
        return {'airlines': airlines,
                'layover': layover_stations,
                'Duration': total_duration,
                'price': price}

# if __name__ == "__main__":
#     print("In flight")
#     flights_tool = Flights()

#     # Define the query parameters as a dictionary
#     query_parameters = {
#         'origin': 'ATL',
#         'destination': 'JFK',
#         'departure_date': '2024-07-27',
#         'return_date': '2024-07-30',
#         'currency': 'USD'
#     }

#     # Pass the entire dictionary as a single positional argument to invoke
#     response = flights_tool.invoke({'query': query_parameters})
#     print(response)
