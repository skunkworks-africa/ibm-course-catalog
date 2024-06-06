import requests
import json
import logging

logging.basicConfig(filename='fetch_and_process_data.log', level=logging.ERROR)

def download_json(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(file_path, 'wb') as file:
            file.write(response.content)
        logging.info("JSON file downloaded successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download JSON file: {e}")

class CredlyAPI:
    def __init__(self, base_url, authorization_token):
        self.base_url = base_url
        self.authorization_token = authorization_token
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {authorization_token}',
            'Content-Type': 'application/json'
        }

    def make_request(self, method, endpoint, data=None):
        try:
            response = requests.request(method, f"{self.base_url}/{endpoint}", headers=self.headers, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to make {method} request to {endpoint}: {e}")
            return None

    def get(self, endpoint):
        return self.make_request('GET', endpoint)

    def fetch_badges(self):
        # Fetch badges from Credly
        return self.get("badges")

# Example usage:
if __name__ == "__main__":
    base_url = "https://sandbox.credly.com/v1"  # Sandbox environment
    authorization_token = "your_authorization_token_here"
    
    credly_api = CredlyAPI(base_url, authorization_token)
    badges_data = credly_api.fetch_badges()
    if badges_data:
        print("Badges Data:", badges_data)
    else:
        print("Failed to fetch badges data.")
