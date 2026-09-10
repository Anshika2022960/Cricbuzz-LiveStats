import requests
import os

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("RAPIDAPI_KEY")

BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"


HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
}


def get_live_matches():

    url = f"{BASE_URL}/matches/v1/live"

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:

        print("API Error:", error)

        return None


def get_recent_matches():

    url = f"{BASE_URL}/matches/v1/recent"

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:

        return None


def get_upcoming_matches():

    url = f"{BASE_URL}/matches/v1/upcoming"

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:

        return None