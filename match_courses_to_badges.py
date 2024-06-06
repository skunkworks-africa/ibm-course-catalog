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

    if not courses or not badges:
        logging.warning("Empty courses or badges data.")
        return matched_courses

    for course in courses:
        course_name = course.get('course_name')
        course_badges = []

        for badge in badges:
            badge_name = badge.get('badge_name')
            if course_name in badge_name:
                course_badges.append(badge_name)

        matched_courses[course_name] = course_badges

    return matched_courses

def main():
    url = "https://www.ibm.com/training/files/GTPjson/CourseFeed_Global.json"
    file_path = "course_feed.json"

    download_json(url, file_path)

    courses_data = load_json(file_path)

    if not courses_data:
        logging.error("Failed to load courses data.")
        return

    badges_file_path = "badges.json"
    badges_data = load_json(badges_file_path)

    if not badges_data:
        logging.error("Failed to load badges data.")
        return

    matched_courses = match_courses_to_badges(courses_data, badges_data)

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
