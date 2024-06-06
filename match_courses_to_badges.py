import requests
import json

# Function to download the JSON file
def download_json(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def match_courses_to_badges(courses, badges):
    # Matching logic goes here
    pass

def main():
    # URL of the JSON file containing IBM course data
    url = "https://www.ibm.com/training/files/GTPjson/CourseFeed_Global.json"
    
    # File path where you want to save the downloaded JSON file
    file_path = "course_feed.json"

    # Download the JSON file
    download_json(url, file_path)

    print("Course feed JSON file downloaded successfully.")

    # Load IBM courses data
    courses_data = load_json(file_path)

    # Load Credly badges data
    badges_data = load_json('badges.json')

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
