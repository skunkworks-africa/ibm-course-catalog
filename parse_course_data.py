import json
import logging

logging.basicConfig(filename='parse_course_data.log', level=logging.ERROR)

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

def extract_courses(data):
    courses = []
    if isinstance(data, dict) and 'courses' in data:
        courses = data['courses']
    else:
        logging.error("Invalid JSON format or missing 'courses' key.")
    return courses

def main():
    file_path = "course_feed.json"
    course_data = load_json(file_path)

    if course_data is None:
        logging.error("Failed to load course data. Exiting.")
        return

    courses = extract_courses(course_data)

    if courses:
        for course in courses:
            print(course)
    else:
        logging.warning("No courses found in the data.")

if __name__ == "__main__":
    main()
