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
        logging.error(f"Failed to download JSON file from {url}: {e}")

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

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        logging.info("JSON file loaded successfully.")
        return data
    except FileNotFoundError as e:
        logging.error(f"JSON file not found: {e}")
        return None
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            logging.error(f"Error decoding JSON file: {e}")
        else:
            logging.error(f"Unexpected error: {e}")
        return None

def match_courses_to_badges(courses, badges):
    matched_courses = {}

    if not isinstance(courses, list) or not isinstance(badges, list):
        logging.error("Invalid input data. Expected lists for courses and badges.")
        return matched_courses
    
    if not courses or not badges:
        logging.warning("Empty courses or badges data.")
        return matched_courses

    try:
        for course in courses:
            if not isinstance(course, dict) or 'course_name' not in course:
                logging.warning("Invalid course data format. Skipping this course.")
                continue

            course_name = course.get('course_name')
            course_badges = []

            for badge in badges:
                if not isinstance(badge, dict) or 'badge_name' not in badge:
                    logging.warning("Invalid badge data format. Skipping this badge.")
                    continue

                badge_name = badge.get('badge_name')
                if course_name in badge_name:
                    course_badges.append(badge_name)

            matched_courses[course_name] = course_badges

        return matched_courses

    except Exception as e:
        logging.error(f"An error occurred while matching courses to badges: {e}")
        return matched_courses

def main():
    base_url = "https://sandbox.credly.com/v1"  # Sandbox environment
    authorization_token = "your_authorization_token_here"
    
    credly_api = CredlyAPI(base_url, authorization_token)
    badges_data = credly_api.fetch_badges()
    if badges_data:
        print("Badges Data:", badges_data)
    else:
        print("Failed to fetch badges data.")

    url = "https://www.ibm.com/training/files/GTPjson/CourseFeed_Global.json"
    file_path = "course_feed.json"

    download_json(url, file_path)
    courses_data = load_json(file_path)

    if courses_data is None:
        logging.error("Failed to fetch or parse courses data. Exiting.")
        return

    badges_file_path = "badges.json"
    badges_data = load_json(badges_file_path)

    if badges_data is None:
        logging.error("Failed to load badges data. Exiting.")
        return

    matched_courses = match_courses_to_badges(courses_data, badges_data)

    if not isinstance(matched_courses, dict):
        logging.error("Error in matching courses to badges. Exiting.")
        return

    for course, badges in matched_courses.items():
        print(f"Course: {course}")
        if badges:
            print("Matched Badges:")
            for badge in badges:
                print(f"- {badge}")
        else:
            print("No matched badges found for this course.")
        print()

if __name__ == "__main__":
    main()
