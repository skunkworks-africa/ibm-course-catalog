import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def match_courses_to_badges(courses, badges):
    matches = {}
    for course in courses:
        course_name = course['name']
        course_description = course.get('description', '')
        matched_badges = []
        for badge in badges:
            badge_name = badge['name']
            badge_description = badge.get('description', '')
            # Example matching logic: check if course name or description contains badge name or description
            if badge_name.lower() in course_name.lower() or badge_name.lower() in course_description.lower() or \
               badge_description.lower() in course_name.lower() or badge_description.lower() in course_description.lower():
                matched_badges.append(badge_name)
        matches[course_name] = matched_badges
    return matches

def main():
    courses_data = load_json('course_feed.json')
    badges_data = load_json('badges.json')

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
