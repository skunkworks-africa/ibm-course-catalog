#!/bin/bash

# Script to update the IBM course catalog

# Download course feed JSON file
python fetch_and_process_data.py

# Parse course data and extract course information
python parse_course_data.py > course_catalog.txt

# Update README.md with table of current courses and badges
python update_readme.py course_catalog.txt

# Commit changes
git add README.md
git commit -m "Updated IBM course catalog"
git push origin master
