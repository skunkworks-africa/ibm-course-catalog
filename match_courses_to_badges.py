import requests
import json
import logging

# Configure logging
logging.basicConfig(filename='fetch_and_process_data.log', level=logging.ERROR)

# Function to download the JSON file
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
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON file: {e}")
        return None

def match_courses_to_badges(courses, badges):
    matched_courses = {}  # Initialize an empty dictionary to store matched courses and badges

    if not courses or not badges:
        logging.warning("Empty courses or badges data.")
        return matched_courses

    # Iterate through courses
    for course in courses:
        course_name = course.get('course_name')  # Get the course name
        course_badges = []  # Initialize an empty list to store matched badges for the current course

        # Iterate through badges
        for badge in badges:
            badge_name = badge.get('badge_name')  # Get the badge name
            # Check if there is a match between course and badge (example condition)
            if course_name in badge_name:
                course_badges.append(badge_name)  # Add the matched badge to the list

        # Add the course and its matched badges to the dictionary
        matched_courses[course_name] = course_badges

    return matched_courses

def main():
    # URL of the JSON file containing IBM course data
    url = "https://www.ibm.com/training/files/GTPjson/CourseFeed_Global.json"
    
    # File path where you want to save the downloaded JSON file
    file_path = "course_feed.json"

    # Download the JSON file
    download_json(url, file_path)

    # Load IBM courses data
    courses_data = load_json(file_path)

    if not courses_data:
        logging.error("Failed to load courses data.")
        return

    # Load Credly badges data (replace 'badges.json' with the actual file path)
    badges_data = load_json('badges.json')

    if not badges_data:
        logging.error("Failed to load badges data.")
        return

    # Match courses to badges
    matched_courses = match_courses_to_badges(courses_data, badges_data)

    # Print or write matched data as needed
    # Example:
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

