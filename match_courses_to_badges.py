import requests
import json
import logging
import time

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

def fetch_and_parse_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch JSON data from {url}: {e}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON data from {url}: {e}")
        return None

def match_courses_to_badges(courses, badges):
    matched_courses = {}  # Initialize an empty dictionary to store matched courses and badges

    # Issue 1: Initialization
    if not isinstance(courses, list) or not isinstance(badges, list):
        logging.error("Invalid input data. Expected lists for courses and badges.")
        return matched_courses
    
    # Issue 2: Empty Data Handling
    if not courses or not badges:
        logging.warning("Empty courses or badges data.")
        return matched_courses

    try:
        # Iterate through courses
        for course in courses:
            if not isinstance(course, dict) or 'course_name' not in course:
                logging.warning("Invalid course data format. Skipping this course.")
                continue

            course_name = course.get('course_name')  # Get the course name
            course_badges = []  # Initialize an empty list to store matched badges for the current course

            # Iterate through badges
            for badge in badges:
                if not isinstance(badge, dict) or 'badge_name' not in badge:
                    logging.warning("Invalid badge data format. Skipping this badge.")
                    continue

                badge_name = badge.get('badge_name')  # Get the badge name
                # Issue 3: Matching Logic
                if course_name in badge_name:
                    course_badges.append(badge_name)  # Add the matched badge to the list

            # Issue 5: Storing Matches
            matched_courses[course_name] = course_badges

        # Issue 6: Returning Results
        return matched_courses

    except Exception as e:
        logging.error(f"An error occurred while matching courses to badges: {e}")
        return matched_courses  # Ensure that matched_courses is always returned, even in case of error

def main():
    url = "https://www.ibm.com/training/files/GTPjson/CourseFeed_Global.json"
    file_path = "course_feed.json"

    # Issue: Error handling for downloading JSON
    download_json(url, file_path)

    # Fetch and parse JSON data
    courses_data = fetch_and_parse_json(url)
    if courses_data is None:
        logging.error("Failed to fetch or parse courses data. Exiting.")
        return

    # Issue: Loading badges data
    badges_file_path = "badges.json"
    badges_data = load_json(badges_file_path)
    if badges_data is None:
        logging.error("Failed to load badges data. Exiting.")
        return

    # Issue: Matching courses to badges
    matched_courses = match_courses_to_badges(courses_data, badges_data)

    # Issue: Error handling for accessing matched_courses
    if not isinstance(matched_courses, dict):
        logging.error("Error in matching courses to badges. Exiting.")
        return

    # Issue: Printing matched courses and badges
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
