# Project Name
## Emlid CSV Orthometric Calculator

# Description:
### This project:
1. Will take a CSV file (data file from an Emlid with ellipsoidal height)
1. Will calculate the orthometric height in meters based off the ellipsoid height, latitude and longitude
1. Will return the geoid height and the orthometric height in meters and feet
1. Will make a new column in the CSV file for geoid height (Geoid Height (m)), ortho height in meters (Orthometric Height (m)) and ortho height in feet (Orthometric Height (ft))

# Dependencies:
1. To run this script, you'll need the following dependencies:

- Python 3.9
- pandas
- pygeodesy
- wxpython

# Installation Instructions:
1. Make sure you have Python 3.9 installed on your machine. You can download it from the official Python website: https://www.python.org/downloads/

2. Install the required Python packages using pip. Open your terminal or command prompt and run the following commands:

    `pip install pandas pygeodesy wxpython`

# Usage:
- When this is properly installed, running the script should bring up a GUI to upload a file.
- Use this GUI to locate the file and you're trying to update and give it a new extension name in the space provided.
- FOR THIS TO WORK CORRECTLY each CSV file MUST HAVE columns labled "Latitude" "Longitude" and "Ellipsoidal height (m)"
