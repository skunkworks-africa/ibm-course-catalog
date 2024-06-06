import requests

# Function to download the JSON file
def download_json(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)

def main():
    # URL of the JSON file containing IBM course data
    url = "https://www.ibm.com/training/files/GTPjson/CourseFeed_Global.json"
    
    # File path where you want to save the downloaded JSON file
    file_path = "course_feed.json"

    # Download the JSON file
    download_json(url, file_path)

    print("Course feed JSON file downloaded successfully.")

    # Your existing code for matching courses to badges can go here

if __name__ == "__main__":
    main()
